#! /usr/bin/python3

# Testing script to build image file for NZ NI with Mapillary and OSM Notes
# Assumes PBF file has been downloaded and split already
#
# TODO: Bounds are hard coded for now
#       Region is hardcoded as oceania_nz_ni
# FIXME:
#        Position of notes when Garmin image file is rendered (but notes.osm looks fine in JOSM, also ok if notes but not Mapillary included in Garmin img)
#        Rendered with text "AAH"
import os

import Mapillary_Download
import OSM_Notes_Download
import Convert2OSM

mapillary_geojson_file = "work/mapillary/oceania_nz_ni/sequences.geojson"
mapillary_osm_file = "work/mapillary/oceania_nz_ni/sequences.osm"

notes_json_file="work/notes/oceania_nz_ni/notes.json"
notes_osm_file = "work/notes/oceania_nz_ni/notes.osm"

west, south, east, north = [174.6999,-36.8795,174.7000,-36.87945]  # Waterview/Pt Chev, 1 Mapillary tile
west, south, east, north = [174.68,-36.9,174.75,-36.85]  # Part of Auckland 20 Mapillary tiles
#west, south, east, north = [174.65,-36.9,174.75,-36.8]  # Part of Auckland 42 Mapillary tiles
#west, south, east, north = [174.5,-36.9,174.8,-36.8]  # Part of Auckland 105 Mapillary tiles
#west, south, east, north = [174.4,-37.1,174.9,-36.7]    # Most of Auckland, 552 Mapillary tiles
#west, south, east, north = [171.721,-38.558,178.665,-34.189]    # North and Central NI
#west, south, east, north = [174.000,-37.500,175.000,-36.500] # ???, 2726 Mapillary tiles


print( "==================================================================================================")
print( "Downloading Mapillary sequences to '{mapillary_geojson_file}' ...")
Mapillary_Download.download(mapillary_geojson_file, west, south, east, north)
print(f"Converting '{mapillary_geojson_file}' to '{mapillary_osm_file}'...")
Convert2OSM.convert(mapillary_geojson_file, mapillary_osm_file)

print( "==================================================================================================")
print( "Downloading OSM notes to '{notes_json_file}' ...")
OSM_Notes_Download.download(notes_json_file, west, south, east, north )
print(f"Converting '{notes_json_file}' to '{notes_osm_file}'...")
Convert2OSM.convert(notes_json_file, notes_osm_file)

# Build Garmin img file from split PBFs
print( "==================================================================================================")
print( "Building image files ...")

print( "   Oceania NZ NI ...")
os.system("build/map.sh -t route -s route -r oceania_nz_ni -m -n")
