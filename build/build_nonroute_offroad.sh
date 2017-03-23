#
# Build non-routeable Garmin maps form OSM data and apply the offroad type rules
#
# TODO:
#     - Add note on how to download OSM pbf file
#     - Add command to split downloaded OSM PBF file
#     - Script this so the user can select to just perform a subset of operations
#     - Pass in a name for the area for which map is built (e.g. oceania_nz_ni) and use this for final file name

# Convert OSM files to Garmin image files
#    - Assumes split OSM pbf files have been put in the directory osmsplitmaps
#java -Xmx1024m -jar tools/mkgmap-r3834/mkgmap.jar --remove-short-arcs --add-pois-to-areas --style-file=build/nonroute.style --precomp-sea=input/sea.zip --generate-sea --output-dir=work/garminsplitmaps work/osmsplitmaps/*.pbf

# Combine all the Garmin image files to a single Garmin gmapsupp image file, applying the offroad type rules
java -Xmx1024m -jar tools/mkgmap-r3834/mkgmap.jar --gmapsupp --product-id=1 --output-dir=work work/garminsplitmaps/6*.img build/offroad.typ

# Move the resulting gmapsupp image files into correct sub-directory and rename
mv work/gmapsupp.img maps/nonroute/oceania_nz_ni.img

# Show size of resulting Garmin image file
ls -lh maps/nonroute/oceania_nz_ni.img
