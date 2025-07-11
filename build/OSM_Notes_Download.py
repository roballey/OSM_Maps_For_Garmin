#
# Download notes from OSM and write them to a JSON file
# See https://wiki.openstreetmap.org/wiki/API_v0.6#Retrieving_notes_data_by_bounding_box:_GET_/api/0.6/notes
# FIXME: BBox is hardcoded
#        Region is hardcoded as oceania_nz_ni
import requests, json

import Convert2OSM

def download(download_file):
  # BBox: Bottom left, top right
  west, south, east, north = [173.5,-37.5,175.5,-36.0]    # Auckland
  
  url = f'https://api.openstreetmap.org/api/0.6/notes.json?bbox={west},{south},{east},{north}&closed=0'
  response = requests.get(url)
         
  f = open(download_file,"wb")
  f.write(response.content)
  f.close()

# -----------------------------------------------------------------------------
json_file="work/notes/oceania_nz_ni/notes.json"
osm_file = "work/notes/oceania_nz_ni/notes.osm"

print( "==================================================================================================")
print(f"Downloading '{json_file}' from OSM Notes...")
download(json_file)

print( "==================================================================================================")
print(f"Converting '{json_file}' to '{osm_file}'...")
Convert2OSM.convert(json_file, osm_file)

