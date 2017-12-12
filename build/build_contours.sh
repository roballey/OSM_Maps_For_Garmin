# Build PBF files of contour data from SRTM data. The SRTM data will be downloaded into a directory named hgt if it is not already there
# This script is copied from: https://wiki.openstreetmap.org/wiki/OSM_Map_on_Garmin/Contours_using_phygtmap
pushd work/contours
rm *.pbf
phyghtmap \
 --step=50 \
 --line-cat=400,100 \
 --polygon=../../input/oceania_nz_ni.poly \
 --hgtdir=../../hgt \
 --pbf \
 --output-prefix=contour
popd
