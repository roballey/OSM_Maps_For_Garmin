#! /bin/sh

# Testing script to build image file for NZ NI with Mapillary and OSM Notes
# Assumes PBF file has been downloaded and split already

# FIXME:
#        Position of notes when Garmin image file is rendered, and rendered with text "AAH"

echo "=================================================================================================="
echo "Downloading Mapillary sequences ..."
python3 build/Mapillary_Download.py

echo "=================================================================================================="
echo "Downloading OSM notes ..."
python3 build/OSM_Notes_Download.py

# Build Garmin img file from split PBFs
echo "=================================================================================================="
echo "Building image files ..."

echo "   Oceania NZ NI ..."
build/map.sh -t route -s route -r oceania_nz_ni -m -n
