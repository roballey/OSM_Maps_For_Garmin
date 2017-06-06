# Build PBF files of contour data from SRTM data. The SRTM data will be downloaded into a directory named hgt if it is not already there
# This script is copied from: https://wiki.openstreetmap.org/wiki/OSM_Map_on_Garmin/Contours_using_phygtmap
phyghtmap \
 --step=20 \
 --line-cat=400,100 \
 --polygon=../data/mymap.poly \
 --pbf \
 --output-prefix=contour

