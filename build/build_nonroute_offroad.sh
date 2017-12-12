#
# Build non-routeable Garmin maps form OSM data and apply the offroad type rules
#
# To download data for Oceania, New Zealand, North Island, use the link:
#   https://extract.bbbike.org/?lang=en&sw_lng=172.609&sw_lat=-41.675&ne_lng=178.618&ne_lat=-34.342&format=osm.pbf&email=alley.rob%40gmail.com&as=38.67661046194356&pg=0.32780147741934773&coords=173.744%2C-39.449%7C173.914%2C-39.53%7C174.185%2C-39.621%7C174.744%2C-39.921%7C175.007%2C-40.015%7C175.176%2C-40.311%7C174.577%2C-41.337%7C174.915%2C-41.431%7C175.105%2C-41.427%7C175.142%2C-41.534%7C175.344%2C-41.675%7C176.203%2C-41.083%7C176.375%2C-40.698%7C176.645%2C-40.487%7C176.901%2C-40.127%7C177.005%2C-39.877%7C177.138%2C-39.635%7C176.943%2C-39.416%7C177.1%2C-39.196%7C177.366%2C-39.086%7C177.65%2C-39.091%7C177.86%2C-39.31%7C177.996%2C-39.21%7C178.026%2C-39.075%7C177.942%2C-39.001%7C178.017%2C-38.718%7C178.107%2C-38.724%7C178.375%2C-38.439%7C178.42%2C-38.015%7C178.618%2C-37.658%7C178.193%2C-37.484%7C177.977%2C-37.529%7C177.761%2C-37.634%7C177.433%2C-37.926%7C177.149%2C-37.961%7C176.635%2C-37.811%7C176.275%2C-37.617%7C176.032%2C-37.447%7C175.954%2C-37.188%7C175.849%2C-36.815%7C175.85%2C-36.594%7C175.751%2C-36.54%7C175.558%2C-36.539%7C175.437%2C-36.419%7C175.585%2C-36.353%7C175.397%2C-36.017%7C175.261%2C-36.044%7C175.328%2C-36.338%7C175.294%2C-36.499%7C175.422%2C-36.715%7C175.298%2C-36.817%7C175.023%2C-36.635%7C175.149%2C-36.262%7C175.131%2C-36.153%7C175.02%2C-36.216%7C174.953%2C-36.618%7C174.848%2C-36.314%7C174.71%2C-36.129%7C174.796%2C-36.01%7C174.745%2C-35.933%7C174.666%2C-35.861%7C174.569%2C-35.589%7C174.338%2C-35.165%7C174.186%2C-35.184%7C174.061%2C-35.069%7C173.867%2C-34.914%7C173.552%2C-34.864%7C173.502%2C-34.759%7C173.247%2C-34.803%7C173.099%2C-34.665%7C173.045%2C-34.342%7C172.809%2C-34.412%7C172.609%2C-34.411%7C173.137%2C-35.053%7C173.027%2C-35.198%7C173.479%2C-35.716%7C173.799%2C-36.059%7C174.085%2C-36.448%7C174.511%2C-37.093%7C174.77%2C-37.754%7C174.652%2C-38.097%7C174.654%2C-38.267%7C174.572%2C-38.614%7C174.449%2C-38.887%7C173.797%2C-39.109%7C173.735%2C-39.279&oi=1&layers=B000T&city=oceania_nz_ni&submit=extract&expire=1490258470 
#  or:
#   https://extract.bbbike.org/?sw_lng=172.609&sw_lat=-41.675&ne_lng=178.618&ne_lat=-34.342&format=osm.pbf&coords=173.744%2C-39.449%7C173.914%2C-39.53%7C174.185%2C-39.621%7C174.744%2C-39.921%7C175.007%2C-40.015%7C175.176%2C-40.311%7C174.577%2C-41.337%7C174.915%2C-41.431%7C175.105%2C-41.427%7C175.142%2C-41.534%7C175.344%2C-41.675%7C176.203%2C-41.083%7C176.375%2C-40.698%7C176.645%2C-40.487%7C176.901%2C-40.127%7C177.005%2C-39.877%7C177.138%2C-39.635%7C176.943%2C-39.416%7C177.1%2C-39.196%7C177.366%2C-39.086%7C177.65%2C-39.091%7C177.86%2C-39.31%7C177.996%2C-39.21%7C178.026%2C-39.075%7C177.942%2C-39.001%7C178.017%2C-38.718%7C178.107%2C-38.724%7C178.375%2C-38.439%7C178.42%2C-38.015%7C178.618%2C-37.658%7C178.193%2C-37.484%7C177.977%2C-37.529%7C177.761%2C-37.634%7C177.433%2C-37.926%7C177.149%2C-37.961%7C176.635%2C-37.811%7C176.275%2C-37.617%7C176.032%2C-37.447%7C175.954%2C-37.188%7C175.849%2C-36.815%7C175.85%2C-36.594%7C175.751%2C-36.54%7C175.558%2C-36.539%7C175.437%2C-36.419%7C175.585%2C-36.353%7C175.397%2C-36.017%7C175.261%2C-36.044%7C175.328%2C-36.338%7C175.294%2C-36.499%7C175.422%2C-36.715%7C175.298%2C-36.817%7C175.023%2C-36.635%7C175.149%2C-36.262%7C175.131%2C-36.153%7C175.02%2C-36.216%7C174.953%2C-36.618%7C174.848%2C-36.314%7C174.71%2C-36.129%7C174.796%2C-36.01%7C174.745%2C-35.933%7C174.666%2C-35.861%7C174.569%2C-35.589%7C174.338%2C-35.165%7C174.186%2C-35.184%7C174.061%2C-35.069%7C173.867%2C-34.914%7C173.552%2C-34.864%7C173.502%2C-34.759%7C173.247%2C-34.803%7C173.099%2C-34.665%7C173.045%2C-34.342%7C172.809%2C-34.412%7C172.609%2C-34.411%7C173.137%2C-35.053%7C173.027%2C-35.198%7C173.479%2C-35.716%7C173.799%2C-36.059%7C174.085%2C-36.448%7C174.511%2C-37.093%7C174.77%2C-37.754%7C174.652%2C-38.097%7C174.654%2C-38.267%7C174.572%2C-38.614%7C174.449%2C-38.887%7C173.797%2C-39.109%7C173.735%2C-39.279&city=oceania_nz_ni
#

# first remove any previously generated Garmin image files so as to not pollute the output
rm work/garminsplitmaps/*.img

# Convert split OSM files and countours to split Garmin image files
#    - Assumes split OSM pbf files have been put in the directory work/osmsplitmaps
#    - Assumes contour pbf files have been put in the directory work/contours
echo "Converting split OSM files and contours into Garmin Image files ..."
java -Xmx1024m -jar tools/mkgmap-r3834/mkgmap.jar --remove-short-arcs --add-pois-to-areas --style-file=build/nonroute.style --precomp-sea=input/sea.zip --generate-sea --output-dir=work/garminsplitmaps work/osmsplitmaps/*.pbf work/contours/*.pbf

# Combine all the Garmin image files to a single Garmin gmapsupp image file, applying the offroad type rules
echo "Combining Garmin Image files ..."
java -Xmx1024m -jar tools/mkgmap-r3834/mkgmap.jar --gmapsupp --product-id=1 --output-dir=work work/garminsplitmaps/6*.img build/offroad.typ

# Remove previously generated Garmin image files so as to not pollute the output
rm maps/nonroute/oceania_nz_ni.img
# Also remove the files generated by the build_tdb script so versions aren't mixed
rm maps/nonroute/osmmap.*
rm maps/nonroute/offroad.typ


# Move the resulting gmapsupp image files into correct sub-directory and rename
mv work/gmapsupp.img maps/nonroute/oceania_nz_ni.img

# Show size of resulting Garmin image file
ls -lh maps/nonroute/oceania_nz_ni.img
