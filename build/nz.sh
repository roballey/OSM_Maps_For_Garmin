#! /bin/sh

# Download all of NZ pbf
echo "Downloading ..."
wget https://download.geofabrik.de/australia-oceania/new-zealand-latest.osm.pbf --output-document=input/oceania_nz.pbf

# Split input file, cropping to only NI
echo "Splitting ..."
build/split.sh -r oceania_nz_ni -p oceania_nz_ni.poly -i oceania_nz.pbf
build/split.sh -r oceania_nz_si -p oceania_nz_si.poly -i oceania_nz.pbf

# Build Garmin img files from split PBFs
echo "Building image files ..."
build/map.sh -t nonroute -s nonroute -r oceania_nz_ni
build/map.sh -t route -s route -r oceania_nz_ni

build/map.sh -t nonroute -s nonroute -r oceania_nz_si
build/map.sh -t route -s route -r oceania_nz_si
