#! /usr/bin/python3

# Build Garmin IMG files from OSM data.
# Download inputs (OSM data and optionally Mapillary sequences and OSM notes), splits inputs, and builds IMG files
#
# FIXME: Lots of functions are building path names, pass in instead
# FIXME: Only get bounding box once

import argparse
import json
import os
from datetime import datetime

import Mapillary_Coverage
import OSM_Notes

java_memory="8000m"

#------------------------------------------------------------------------------
# Download OSM map data PBF file
def download_osm(url, output_file):
        print(f"    Downloading OSM map data from '{url}'...")
        os.system(f"wget {url} --output-document=downloads/{output_file}")

#------------------------------------------------------------------------------
# Split source PBF
def split(region, poly_file, source_pbf_file):
    options=""
    split_dir=f"work/osmsplitmaps/{region}"
    if not poly_file:
        print(f"    Splitting '{source_pbf_file}' for {region}")
    else:
        options=options + f"--polygon-file=poly/{poly_file}";
        print(f"    Splitting '{source_pbf_file}' for {region} limiting by '{poly_file}'")
    print(f"    Output to {split_dir}")
    os.system(f"java -Xmx{java_memory} -jar tools/splitter-*/splitter.jar downloads/{source_pbf_file} {options} --output-dir={split_dir} > logs/split.log")

#------------------------------------------------------------------------------
# Get bounding box from a POLY file (assumes only 1 area specified in POLY file)
def get_bounding_box(poly_file):
  file=open(poly_file, "r")
  
  south=90.0
  north=-90.0
  west=180.0
  east=-180.0
  
  in_section=False
  for (index, line) in enumerate(file.readlines()):
      #print(index, line)
  
      # Skip first line (name of file)
      if index == 0:
          pass
      # Ignore END of section and file
      elif line.strip() == "END":
         in_section=False
      # First line of section defines the section name
      elif not in_section:
          in_section=True
      else:
        (long, lat) = line.split()
  
        south=min(south,float(lat))
        north=max(north,float(lat))
        west=min(west,float(long))
        east=max(east,float(long))
  file.close()
  return(west, south, east, north)

#------------------------------------------------------------------------------
# Build Garmin IMG files
def build(region, map_type, map_style, args):
    tmp_dir="work/tmp"
    input_osm_dir=f"work/osmsplitmaps/{region}"
    input_mapillary_filename=f"downloads/mapillary/{region}/sequences.osm"
    input_notes_filename=f"downloads/notes/{region}/notes.osm"
    output_dir=f"maps/{map_style}/{region}"
    version=datetime.now().strftime('%y%m')

    if not os.path.exists(output_dir):
        os.makedirs(output_dir);
        print(f"    Output directory '{output_dir}' did not exist, created")

    input_files=os.path.join(input_osm_dir, "*.pbf")
    print(f"    Building Garmin IMG version {version} for {region} using style {map_style} and type {map_type}")
    print(f"      Using OSM data from '{input_osm_dir}'")

    if args.mapillary:
        print(f"      Including Mapillary coverage data from '{input_mapillary_filename}'")
        input_files = input_files + f" {input_mapillary_filename}"
    if args.notes:
        print(f"      Including OSM notes data from '{input_notes_filename}'")
        input_files = input_files + f" {input_notes_filename}"

    print(f"\n      Converting TYP file from text...")
    os.system(f"java -Xmx{java_memory} -jar tools/mkgmap-r*/mkgmap.jar --output-dir={tmp_dir} type/{map_type}.txt")

    print(f"\n      Building IMG file '{output_dir}/gmapsupp.img'...")
    os.system(f"java -Xmx{java_memory} -jar tools/mkgmap-r*/mkgmap.jar \
                    --family-name='OSM for Garmin' \
                    --series-name='{map_type}' \
		            --description='OSM maps for Garmin devices' \
		            --product-version=version \
		            --region-name='Oceania' \
                    --country-name='New Zealand' \
                    --country-abbr='NZ' \
		            --drive-on=left \
                    --index \
                    --housenumbers \
                    --route \
                    --adjust-turn-headings \
                    --add-pois-to-areas \
                    --make-opposite-cycleways \
                    --link-pois-to-ways \
                    --process-destination \
                    --process-exits \
                    --remove-short-arcs \
                    --gmapsupp \
                    --product-id=1 \
                    --style-file=styles/{map_style}.style \
                    --precomp-sea=downloads/sea-latest.zip \
                    --generate-sea \
                    --output-dir={output_dir} \
                      {input_files} \
                      {tmp_dir}/{map_type}.typ" )

    # TODO: Clean up <num>.img; ovm*.img and osmmap.img files created in output_dir

#------------------------------------------------------------------------------
# Create hard links to image files for QMapShack
def create_link(img_file, linked_file):
   print(f"    Link '{img_file}' to '{linked_file}'")
   if os.path.exists(linked_file):
       os.remove(linked_file)
   os.link(img_file,linked_file)

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
        print( "=== Download OSM map data ...")
        for i in config['downloads']:
                download_osm(i['dl'], i['pbf'])
else:
    print( "==================================================================================================")
    print( "--- Skipping OSM map data download step")

# Split OSM PBF file for each region
if not args.no_split:
        print( "==================================================================================================")
        print( "=== Splitting OSM map data PBF files ...")
        for i in config['regions']:
            split(i['region'], i['poly'], i['pbf'])
else:
    print( "==================================================================================================")
    print( "--- Skipping split step")

# Download Mapillary coverage if being included in map
# TODO: Currently just draws Mapillary sequence lines over the top of OSM data.  Change to simplify Mapillary
#       sequences to a single line each.  Re colour those OSM ways that have a corresponding Mapillary sequence line?
if args.mapillary:
    if not (args.no_download_mapillary or args.no_download):
        print( "==================================================================================================")
        print( "=== Downloading Mapillary coverage data ...")
        for i in config['regions']:
            #west, south, east, north = [174.68,-36.9,174.75,-36.85]  # Part of Auckland, 20 Mapillary tiles
            split_dir=f"work/osmsplitmaps/{i['region']}"
            if 'bbox' in i:
                print(f"Bounding box for region {i['region']} from bbox section in config file")
                (west, south, east, north) = i['bbox']
            elif i['poly']:
                print(f"Bounding box for region {i['region']} from POLY file '{i['poly']}'")
                (west, south, east, north) = get_bounding_box(os.path.join("poly",i['poly']))
            elif os.path.exists(os.path.join(split_dir,"areas.poly")):
                print(f"Bounding box for region {i['region']} from split areas POLY file")
                (west, south, east, north) = get_bounding_box(os.path.join(split_dir,"areas.poly"))
            else:
                quit("Must specify a bbox, a poly file or have performed split if including Mapillary coverage")

            mapillary_dir = f"downloads/mapillary/{i['region']}"
            if not os.path.exists(mapillary_dir):
                os.makedirs(mapillary_dir);
                print(f"    Mapillary directory '{mapillary_dir}' did not exist, created")
            mapillary_geojson_file = f"{mapillary_dir}/sequences.geojson"
            mapillary_osm_file = f"{mapillary_dir}/sequences.osm"

            print(f"Downloading Mapillary sequences to '{mapillary_geojson_file}' ...")
            Mapillary_Coverage.download(mapillary_geojson_file, west, south, east, north)
            print(f"Converting '{mapillary_geojson_file}' to '{mapillary_osm_file}'...")
            Mapillary_Coverage.convert(mapillary_geojson_file, mapillary_osm_file)
    else:
        print( "==================================================================================================")
        print( "--- Skipping Mapillary coverage download")

# Download OSM notes if being included in map
if args.notes:
    if not (args.no_download_notes or args.no_download):
        print( "==================================================================================================")
        print( "=== Downloading OSM notes data ...")
        for i in config['regions']:
            split_dir=f"work/osmsplitmaps/{i['region']}"
            if 'bbox' in i:
                print(f"Bounding box for region {i['region']} from bbox section in config file")
                (west, south, east, north) = i['bbox']
            elif i['poly']:
                print(f"Bounding box for region {i['region']} from POLY file '{i['poly']}'")
                (west, south, east, north) = get_bounding_box(os.path.join("poly",i['poly']))
            elif os.path.exists(os.path.join(split_dir,"areas.poly")):
                print(f"Bounding box for region {i['region']} from split areas POLY file")
                (west, south, east, north) = get_bounding_box(os.path.join(split_dir,"areas.poly"))
            else:
                quit("Must specify a bbox, a poly file or have performed split if including OSM notes data")


            notes_dir = f"downloads/notes/{i['region']}"
            if not os.path.exists(notes_dir):
                os.makedirs(notes_dir);
                print(f"    OSM notes data directory '{notes_dir}' did not exist, created")
            notes_json_file = f"{notes_dir}/notes.json"
            notes_osm_file = f"{notes_dir}/notes.osm"

            print(f"    Downloading OSM notes data as '{notes_json_file}' ...")
            OSM_Notes.download(notes_json_file, west, south, east, north)
            print(f"    Converting OSM notes data from '{notes_json_file}' to '{notes_osm_file}'...")
            OSM_Notes.convert_json_notes_to_osm(notes_json_file, notes_osm_file)
    else:
        print( "==================================================================================================")
        print( "--- Skipping OSM notes download")


# Build Garmin img files from split PBFs
if not args.no_build:
        print( "==================================================================================================")
        print( "=== Building image files ...")
        for i in config['regions']:
                for variant in config['variants']:
                        build(i['region'], variant['style'], variant['type'], args)
else:
    print( "==================================================================================================")
    print( "--- Skipping build step")

print( "==================================================================================================")
print( "=== Creating links to image files ...")
link_dir="links"
if not os.path.exists(link_dir):
    os.makedirs(link_dir);
for i in config['regions']:
        region=i['region']
        for variant in config['variants']:
            map_style=variant['style']
            img_file=f"maps/{map_style}/{region}/gmapsupp.img"

            if os.path.exists(img_file):
                linked_file=link_dir+"/"+f"{map_style}/{region}".replace("/","-")+".img"
                create_link(img_file,linked_file)
            else:
                print(f"--- Image file '{img_file}' does not exist")
