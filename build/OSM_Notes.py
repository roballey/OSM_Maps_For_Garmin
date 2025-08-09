#=============================================================================
# Download OSM notes data via OSM API and convert downloaded JSON format
# file to a simplified OSM (XML) file that is handled by mkgmap 

import requests, json
from xml.dom import minidom

#------------------------------------------------------------------------------
# Download notes from OSM and write them to a JSON file
# See https://wiki.openstreetmap.org/wiki/API_v0.6#Retrieving_notes_data_by_bounding_box:_GET_/api/0.6/notes
def download(download_file, west, south, east, north):
  
  url = f'https://api.openstreetmap.org/api/0.6/notes.json?bbox={west},{south},{east},{north}&closed=0'
  response = requests.get(url)
         
  f = open(download_file,"wb")
  f.write(response.content)
  f.close()

#------------------------------------------------------------------------------
# Convert OSM notes data JSON file to OSM file (XML)
def convert_json_notes_to_osm(json_filename, osm_filename):
  notes = json.load(open(json_filename, "r"))
  
  # Create XML using minidom
  xml = minidom.Document()
  osm = xml.createElement('osm')
  osm.setAttribute('version', '0.6')
  osm.setAttribute('generator', 'OSM_for_garmin')
  osm.setAttribute('upload', 'false')
  xml.appendChild(osm )
  
  id=0
  for note in notes['features']:
      for comment in note['properties']['comments']:
          id = id - 1
          node = xml.createElement('node')
          node.setAttribute('visible', 'true')
          node.setAttribute('id', f"{id}")
          node.setAttribute('lat', f"{note['geometry']['coordinates'][1]}")
          node.setAttribute('lon', f"{note['geometry']['coordinates'][0]}")
          osm.appendChild(node)
          tag = xml.createElement('tag')
          tag.setAttribute('k', 'id')
          tag.setAttribute('v', f"{note['properties']['id']}")
          node.appendChild(tag)
          tag = xml.createElement('tag')
          tag.setAttribute('k', 'comments')
          tag.setAttribute('v', f"{comment['text'].splitlines()[0]}")
          node.appendChild(tag)
  
  xml_str = xml.toprettyxml(indent ="  ") 
  with open(osm_filename, "w") as f:
      f.write(xml_str)

