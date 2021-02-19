#! /bin/sh

# Download latest OSM data and build Garmin GPS supplementary map images for whole of NZ
# plus just NI and SI.  Builds routable and non-routeable versions

# Download all of NZ pbf
echo "Downloading ..."
wget https://download.geofabrik.de/australia-oceania/new-zealand-latest.osm.pbf --output-document=input/oceania_nz.pbf

# Split input file, for whole of NZ and also cropped to only NI and SI
echo "Splitting ..."
build/split.sh -r oceania_nz -p oceania_nz.poly -i oceania_nz.pbf
build/split.sh -r oceania_nz_ni -p oceania_nz_ni.poly -i oceania_nz.pbf
build/split.sh -r oceania_nz_si -p oceania_nz_si.poly -i oceania_nz.pbf

# Build Garmin img files from split PBFs
echo "Building image files ..."
echo "   Oceania NZ ..."
build/map.sh -t nonroute -s nonroute -r oceania_nz
build/map.sh -t route -s route -r oceania_nz

echo "   Oceania NZ NI ..."
build/map.sh -t nonroute -s nonroute -r oceania_nz_ni
build/map.sh -t route -s route -r oceania_nz_ni

echo "   Oceania NZ SI ..."
build/map.sh -t nonroute -s nonroute -r oceania_nz_si
build/map.sh -t route -s route -r oceania_nz_si
