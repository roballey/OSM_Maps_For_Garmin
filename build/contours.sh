#! /bin/bash
# Build PBF files of contour lines from Viewfinder data. The Viewfinder data will be downloaded into the hgtdir directory if it is not already there
# This script is based on: https://wiki.openstreetmap.org/wiki/OSM_Map_on_Garmin/Contours_using_phygtmap
#
# NOTE: OSM data must have been downloaded and split before running this script as it relies on the ploygon file written by the split script (build/split.sh)

# Set the name of the region being generated
region="oceania_nz_ni"
region="oceania_nz"

contour_dir="work/contours/${region}"

# Create directory (including parent directories) if it doesn't exist
mkdir -p ${contour_dir}

pushd ${contour_dir}

echo "Removing existing contour pbf files..."
rm *.pbf

echo "Generating contour pbf files from Viewfinder data..."
phyghtmap \
 --source=view1,view3 \
 --step=20 \
 --line-cat=200,100 \
 --polygon=../../osmsplitmaps/${region}/areas.poly \
 --hgtdir=../../../hgt \
 --pbf \
 --output-prefix=contour
popd
