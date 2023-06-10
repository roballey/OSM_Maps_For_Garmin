#! /bin/sh

# Download latest OSM data and build Garmin GPS supplementary map images for South Africa

# Download pbf
echo "Downloading ..."
wget https://download.geofabrik.de/africa/south-africa-latest.osm.pbf --output-document=input/south-africa.pbf

# Split input file
echo "--- Splitting ..."
build/split.sh -r south-africa -i south-africa.pbf

# Build Garmin img files from split PBFs
echo "--- Building image file ..."
echo "---    South Africa ..."
build/map.sh -t route -s route -r south-africa

