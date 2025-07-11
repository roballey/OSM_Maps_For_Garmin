#
# Download notes from OSM and write them to a JSON file
# See https://wiki.openstreetmap.org/wiki/API_v0.6#Retrieving_notes_data_by_bounding_box:_GET_/api/0.6/notes
import requests, json

import Convert2OSM

def download(download_file, west, south, east, north):
  
  url = f'https://api.openstreetmap.org/api/0.6/notes.json?bbox={west},{south},{east},{north}&closed=0'
  response = requests.get(url)
         
  f = open(download_file,"wb")
  f.write(response.content)
  f.close()
