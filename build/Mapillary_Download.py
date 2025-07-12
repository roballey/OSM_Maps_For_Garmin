# 11-Jul-2025
# Based on code from https://gist.github.com/cbeddow `mapillary_sequence_download.py`
# Requires a token from https://www.mapillary.com/dashboard/developers in JSON file ~/mapillary_token.json

# Import modules from standard locations
import os,sys
import mercantile, mapbox_vector_tile, requests, json
from vt2geojson.tools import vt_bytes_to_geojson
from tqdm import tqdm
from pathlib import Path

# -----------------------------------------------------------------------------
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
