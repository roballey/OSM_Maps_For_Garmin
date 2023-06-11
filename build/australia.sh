#! /bin/sh

# Download latest OSM data and build Garmin GPS supplementary map images for Australia

# Download pbf
echo "Downloading ..."
wget https://download.geofabrik.de/australia-oceania/australia-latest.osm.pbf --output-document=input/australia.pbf

# Split input file
echo "--- Splitting ..."
build/split.sh -r australia -i australia.pbf

# Build Garmin img files from split PBFs
echo "--- Building image file ..."
echo "---    Australia ..."
build/map.sh -t route -s route -r australia

