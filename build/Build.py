#! /usr/bin/python3

# Python top level script to download inputs, split, and build images

import argparse
import json
import os

import Mapillary_Download
import OSM_Notes_Download
import Convert2OSM

#------------------------------------------------------------------------------
# Download PBF file
# TODO: Use python module to download ISO using wget via os.system?
def download_osm(url, output_file):
        print(f"    Downloading OSM data from '{url}'...")
        os.system(f"wget {url} --output-document=input/{output_file}")

#------------------------------------------------------------------------------
# WIP: split source PBF
# TODO: Re-implement split.sh in python ISO using os.system
# TODO: Make poly optional
def split(region, poly, source_pbf):
        print(f"    Splitting {source_pbf} for {region} limiting by {poly}")
        os.system(f"build/split.sh -r {region} -p {poly} -i {source_pbf}")

#------------------------------------------------------------------------------
# WIP: Build Garmin IMG files
# TODO: Re-implement map.sh in python ISO using os.system
def build(region, map_type, map_style, args):
    options=""
    print(f"    Building Garmin IMG for {region} using style {map_style} and type {map_type}")
    if args.mapillary:
        options = options + " -m"
    if args.notes:
        options = options + " -n"
    os.system(f"build/map.sh -t {map_type} -s {map_style} -r {region} {options}")

#==============================================================================
parser = argparse.ArgumentParser(
                    prog='Build',
                    description='Build Garmin IMG files from OSM data')

parser.add_argument('config_file', help="Name of JSON config file")
parser.add_argument('-m', '--mapillary', help="Experimental: Include Mapillary coverage",
                    action='store_true') 
parser.add_argument('-n', '--notes', help="Experimental: Include OSM notes",
                    action='store_true') 
parser.add_argument('-nb', '--no-build', help="Don't build the Garmin IMG file",
                    action='store_true') 
parser.add_argument('-nd', '--no-download', help="Don't download anything",
                    action='store_true') 
parser.add_argument('-ndm', '--no-download-mapillary', help="Don't download the Mapillary coverage",
                    action='store_true') 
parser.add_argument('-ndn', '--no-download-notes', help="Don't download the OSM notes",
                    action='store_true') 
parser.add_argument('-ndo', '--no-download-osm', help="Don't download the OSM source data",
                    action='store_true') 
parser.add_argument('-ns', '--no-split', help="don't split the osm source data pbf file",
                    action='store_true') 

args = parser.parse_args()

config = json.load(open(args.config_file, "r"))

# Download OSM PBF files
if not (args.no_download_osm or args.no_download):
        print( "==================================================================================================")
        for i in config['downloads']:
                download_osm(i['dl'], i['pbf'])
else:
    print( "==================================================================================================")
    print( "=== Skipping OSM download step")

# Download Mapillary coverage if being included in map
if args.mapillary:
    if not (args.no_download_mapillary or args.no_download):
        print( "==================================================================================================")
        for i in config['regions']:
            # FIXME: Get bounding box from poly file ISO hardcoding
            west, south, east, north = [174.68,-36.9,174.75,-36.85]  # Part of Auckland, 20 Mapillary tiles
            mapillary_dir = f"work/mapillary/{i['region']}"
            if not os.path.exists(mapillary_dir):
                # FIXME: Create directory ISO quitting
                quit(f"Mapillary directory '{mapillary_dir}' does not exist")
            mapillary_geojson_file = f"{mapillary_dir}/sequences.geojson"
            mapillary_osm_file = f"{mapillary_dir}/sequences.osm"

            print(f"Downloading Mapillary sequences to '{mapillary_geojson_file}' ...")
            Mapillary_Download.download(mapillary_geojson_file, west, south, east, north)
            print(f"Converting '{mapillary_geojson_file}' to '{mapillary_osm_file}'...")
            Convert2OSM.convert(mapillary_geojson_file, mapillary_osm_file)
    else:
        print( "==================================================================================================")
        print( "=== Skipping Mapillary coverage download")

# Download OSM notes if being included in map
if args.notes:
    if not (args.no_download_notes or args.no_download):
        print( "==================================================================================================")
        print( "=== Downloading OSM notes ...")
        for i in config['regions']:
            # FIXME: Get bounding box from poly file ISO hardcoding
            west, south, east, north = [174.68,-36.9,174.75,-36.85]  # Part of Auckland
            notes_dir = f"work/notes/{i['region']}"
            if not os.path.exists(notes_dir):
                # FIXME: Create directory ISO quitting
                quit(f"OSM Notes directory '{notes_dir}' does not exist")
            notes_json_file = f"{notes_dir}/notes.json"
            notes_osm_file = f"{notes_dir}/notes.osm"

            OSM_Notes_Download.download(notes_json_file, west, south, east, north)
            Convert2OSM.convert(notes_json_file, notes_osm_file)
    else:
        print( "==================================================================================================")
        print( "=== Skipping OSM notes download")



# Split PBF file for each region
if not args.no_split:
        print( "==================================================================================================")
        print( "=== Splitting PBF files ...")
        for i in config['regions']:
                split(i['region'], i['poly'], i['pbf'])
else:
    print( "==================================================================================================")
    print( "=== Skipping split step")

# Build Garmin img files from split PBFs
if not args.no_build:
        print( "==================================================================================================")
        print( "=== Building image files ...")
        for i in config['regions']:
                for variant in config['variants']:
                        # FIXME: Build options string here and pass that ISO args
                        build(i['region'], variant['style'], variant['type'], args)
else:
    print( "==================================================================================================")
    print( "=== Skipping build step")
