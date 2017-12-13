# Build PBF files of contour lines from SRTM data. The SRTM data will be downloaded into the hgtdir directory if it is not already there
# This script is based on: https://wiki.openstreetmap.org/wiki/OSM_Map_on_Garmin/Contours_using_phygtmap

# Set the name of the region being generated
region="oceania_nz_ni"

contour_dir="work/contours/${region}"

# Create directory (including parent directories) if it doesn't exist
mkdir -p ${garmin_work_dir}

pushd ${contour_dir}

echo "Removing existing contour pbf files..."
rm *.pbf

echo "Generating contour pbf files from SRTM data..."
phyghtmap \
 --step=50 \
 --line-cat=400,100 \
 --polygon=../../../input/oceania_nz_ni.poly \
 --hgtdir=../../../hgt \
 --pbf \
 --output-prefix=contour
popd
