#! /usr/bin/python3

# Build Garmin IMG files from OSM data.
# Download inputs (OSM data and optionally Mapillary sequences and OSM notes), splitis inputs, and builds IMG files

import argparse
import json
import os
from datetime import datetime

import Mapillary_Download
import OSM_Notes_Download
import Convert2OSM

java_memory="8000m"

#------------------------------------------------------------------------------
# Download PBF file
# TODO: Use python module to download ISO using wget via os.system?
def download_osm(url, output_file):
        print(f"    Downloading OSM data from '{url}'...")
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
    os.system(f"java -Xmx{java_memory} -jar tools/splitter-*/splitter.jar downloads/{source_pbf_file} {options} --output-dir={split_dir} > logs/split.log")

#------------------------------------------------------------------------------
# Get bounding pox from a POLY file (assumes only 1 area specified in POLY file)
def Get_Bounding_Box(poly_file):
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
  print(f"West {west} South {south} East {east} North {north}")
  return(west, south, east, north)

#------------------------------------------------------------------------------
# Build Garmin IMG files
def build(region, map_type, map_style, args):
    tmp_dir="work/tmp"
    input_osm_dir=f"work/osmsplitmaps/{region}"
    input_mapillary_dir=f"downloads/mapillary/{region}/sequences.osm"
    input_notes_dir=f"downloads/notes/{region}/notes.osm"
    output_dir=f"maps/{map_style}/{region}"
    version=datetime.now().strftime('%y%m')

    input_files=os.path.join(input_osm_dir, "*.pbf")

    if not os.path.exists(output_dir):
        os.makedirs(output_dir);
        print(f"    Output directory '{output_dir}' did not exist, created")

    print(f"    Building Garmin IMG version {version} for {region} using style {map_style} and type {map_type}")
    if args.mapillary:
        input_files = input_files + f" {input_mapillary_dir}"
    if args.notes:
        input_files = input_files + f" {input_notes_dir}"

    print(f"      Converting TYP file from text...")
    os.system(f"java -Xmx{java_memory} -jar tools/mkgmap-r*/mkgmap.jar --output-dir={tmp_dir} type/{map_type}.txt")

    print(f"      Building IMG file '{output_dir}/gmapsupp.img'...")
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

# Split OSM PBF file for each region
if not args.no_split:
        print( "==================================================================================================")
        print( "=== Splitting OSM PBF files ...")
        for i in config['regions']:
            split(i['region'], i['poly'], i['pbf'])
else:
    print( "==================================================================================================")
    print( "=== Skipping split step")

# Download Mapillary coverage if being included in map
if args.mapillary:
    if not (args.no_download_mapillary or args.no_download):
        print( "==================================================================================================")
        for i in config['regions']:
            #west, south, east, north = [174.68,-36.9,174.75,-36.85]  # Part of Auckland, 20 Mapillary tiles
            split_dir=f"work/osmsplitmaps/{i['region']}"
            if 'bbox' in i:
                print(f"Bounding box for region {i['region']} from bbox section in config file")
                (west, south, east, north) = i['bbox']
                print(f"West {west} South {south} East {east} North {north}")
            elif i['poly']:
                print(f"Bounding box for region {i['region']} from POLY file '{i['poly']}'")
                (west, south, east, north) = Get_Bounding_Box(os.path.join("poly",i['poly']))
            elif os.path.exists(os.path.join(split_dir,"areas.poly")):
                print(f"Bounding box for region {i['region']} from split areas POLY file")
                (west, south, east, north) = Get_Bounding_Box(os.path.join(split_dir,"areas.poly"))
            else:
                quit("Must specify a bbox, a poly file or have performed split if including Mapillary coverage")

            mapillary_dir = f"downloads/mapillary/{i['region']}"
            if not os.path.exists(mapillary_dir):
                os.makedirs(mapillary_dir);
                print(f"    Mapillary directory '{mapillary_dir}' did not exist, created")
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
            notes_dir = f"downloads/notes/{i['region']}"
            if not os.path.exists(notes_dir):
                os.makedirs(notes_dir);
                print(f"    OSM notes directory '{notes_dir}' did not exist, created")
            notes_json_file = f"{notes_dir}/notes.json"
            notes_osm_file = f"{notes_dir}/notes.osm"

            OSM_Notes_Download.download(notes_json_file, west, south, east, north)
            Convert2OSM.convert(notes_json_file, notes_osm_file)
    else:
        print( "==================================================================================================")
        print( "=== Skipping OSM notes download")


# Build Garmin img files from split PBFs
if not args.no_build:
        print( "==================================================================================================")
        print( "=== Building image files ...")
        for i in config['regions']:
                for variant in config['variants']:
                        build(i['region'], variant['style'], variant['type'], args)
else:
    print( "==================================================================================================")
    print( "=== Skipping build step")
