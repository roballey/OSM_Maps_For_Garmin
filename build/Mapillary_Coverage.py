
# Import modules from standard locations
import os,sys
import mercantile, mapbox_vector_tile, requests, json
from vt2geojson.tools import vt_bytes_to_geojson
from tqdm import tqdm
from pathlib import Path

import logging
import ogr2osm

# -----------------------------------------------------------------------------
# Based on code from https://gist.github.com/cbeddow `mapillary_sequence_download.py`
# Requires a token from https://www.mapillary.com/dashboard/developers in JSON file ~/mapillary_token.json
def download(download_file, west, south, east, north):

  authFile = os.path.join(Path.home(), "mapillary_token.json")
  if not os.path.exists(authFile):
      quit(f"Mapillary token file '{authFile}' not found")
  auth = json.load(open(authFile, "r"))
  
  # define an empty geojson as output
  output= { "type": "FeatureCollection", "features": [] }
  
  # vector tile endpoints -- change this in the API request to reference the correct endpoint
  tile_coverage = 'mly1_public'
  
  # tile layer depends which vector tile endpoints: 
  # 1. if map features or traffic signs, it will be "point" always
  # 2. if looking for coverage, it will be "image" for points, "sequence" for lines, or "overview" for far zoom
  tile_layer = "sequence"
  
  # get the list of tiles with x and y coordinates which intersect our bounding box
  # Zoom is 6-14 inclusive
  tiles = list(mercantile.tiles(west, south, east, north, 14))
  
  with tqdm(total=len(tiles)) as pbar:
      # loop through list of tiles to get tile z/x/y to plug in to Mapillary endpoints and make request
      for tile in tiles:
          tile_url = 'https://tiles.mapillary.com/maps/vtp/{}/2/{}/{}/{}?access_token={}'.format(tile_coverage,tile.z,tile.x,tile.y,auth['token'])
          response = requests.get(tile_url)
          data = vt_bytes_to_geojson(response.content, tile.x, tile.y, tile.z,layer=tile_layer)
  
          pbar.update(1)
  
          # push to output geojson object if yes
          for feature in data['features']:
                  output['features'].append(feature)
  
  # save a local geojson with the filtered data
  with open(download_file, 'w') as f:
      json.dump(output, f)

#------------------------------------------------------------------------------
# Use ogr2osm to convert Mapillary coverage data JSON file to OSM format
# Based on example from https://github.com/roelderickx/ogr2osm
# FIXME: ogr2osm seems a bit heavy weight (handles projection etc), reimplement
# as a simple JSON to OSM (XML) coversion as per OSM_Notes.convert_json_notes_to_osm
def convert(in_file, out_file):
  print(f"    Converting '{in_file}' to '{out_file}'...")
  # 1. Set the logging level of the logger object named 'ogr2osm' to the desired output level
  ogr2osmlogger = logging.getLogger('ogr2osm')
  ogr2osmlogger.setLevel(logging.ERROR)
  ogr2osmlogger.addHandler(logging.StreamHandler())
  
  # 2. Create the translation object. If no translation is required you
  #    can use the base class from ogr2osm, otherwise you need to instantiate
  #    a subclass of ogr2osm.TranslationBase
  translation_object = ogr2osm.TranslationBase()
  
  # 3. Create the ogr datasource. You can specify a source projection but
  #    EPSG:4326 will be assumed if none is given and if the projection of the
  #    datasource is unknown.
  datasource = ogr2osm.OgrDatasource(translation_object)
  # Optional constructor parameters:
  # - source_proj4: --proj4 parameter
  # - source_epsg: --epsg parameter
  # - gisorder: --gis-order parameter
  # - source_encoding: --encoding parameter
  datasource.open_datasource(in_file)
  # Optional open_datasource parameters:
  # - prefer_mem_copy: --no-memory-copy parameter
  
  # 4. Instantiate the ogr to osm converter class ogr2osm.OsmData and start the
  #    conversion process
  osmdata = ogr2osm.OsmData(translation_object)
  # Optional constructor parameters:
  # - rounding_digits: --rounding-digits parameter
  # - significant_digits: --significant-digits parameter
  # - max_points_in_way: --split-ways parameter
  # - add_bounds: --add-bounds parameter
  # - start_id: --id parameter
  # - is_positive: --positive-id parameter
  # - z_value_tagname: --add-z-value-tag
  osmdata.process(datasource)
  
  # 5. Instantiate either ogr2osm.OsmDataWriter or ogr2osm.PbfDataWriter and
  #    invoke output() to write the output file. If required you can write a
  #    custom datawriter class by subclassing ogr2osm.DataWriterBase.
  datawriter = ogr2osm.OsmDataWriter(out_file)
  # Optional constructor parameters:
  # - never_upload: --never-upload parameter
  # - no_upload_false: --no-upload-false parameter
  # - never_download: --never-download parameter
  # - locked: --locked parameter
  # - add_version: --add-version parameter
  # - add_timestamp: --add-timestamp parameter
  # - significant_digits: --significant-digits parameter
  # - suppress_empty_tags: --suppress-empty-tags parameter
  # - max_tag_length: --max-tag-length parameter
  osmdata.output(datawriter)
