# 11-Jul-2025
# Downloading: Based on code from https://gist.github.com/cbeddow `mapillary_sequence_download.py`
# Converting:  Based on example from https://github.com/roelderickx/ogr2osm

# TODO: Bounds are hard coded for now
#       Region is hardcoded as oceania_nz_ni

# Import modules from standard locations
import os,sys
import mercantile, mapbox_vector_tile, requests, json
from vt2geojson.tools import vt_bytes_to_geojson
from tqdm import tqdm

import Convert2OSM

# -----------------------------------------------------------------------------
def download(download_file):

  # Atleast 3.9 required for __file__ to be an absolute path
  if not sys.version_info >= (3, 9):
      quit("ERROR: Python >= 3.9 required")
  
  dir=os.path.dirname(__file__)
  
  authFile = os.path.join(dir, "mapillary_token.json")
  auth = json.load(open(authFile, "r"))
  
  # define an empty geojson as output
  output= { "type": "FeatureCollection", "features": [] }
  
  # vector tile endpoints -- change this in the API request to reference the correct endpoint
  tile_coverage = 'mly1_public'
  
  # tile layer depends which vector tile endpoints: 
  # 1. if map features or traffic signs, it will be "point" always
  # 2. if looking for coverage, it will be "image" for points, "sequence" for lines, or "overview" for far zoom
  tile_layer = "sequence"
  
  west, south, east, north = [174.6999,-36.8795,174.7000,-36.87945]  # Waterview/Pt Chev at zoom 14, 1 tile
  #west, south, east, north = [174.4,-37.1,174.9,-36.7]    # Most of Auckland at zoom 14, 552 tiles
  #west, south, east, north = [171.721,-38.558,178.665,-34.189]    # North and Central NI
  #west, south, east, north = [174.000,-37.500,175.000,-36.500] # Auckland at zoom 14, 2726 tiles
  
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


# -----------------------------------------------------------------------------

geojson_file = "work/mapillary/oceania_nz_ni/sequences.geojson"
osm_file = "work/mapillary/oceania_nz_ni/sequences.osm"

print( "==================================================================================================")
print( "Downloading geojson from Mapillary...")
download(geojson_file)

print( "==================================================================================================")
print(f"Converting '{geojson_file}' to '{osm_file}'...")
Convert2OSM.convert(geojson_file, osm_file)

