#
# Split single PBF file into multiple files for processing via mkgmap
#
rm work/osmsplitmaps/*.osm.pbf
java -Xmx1024m -jar tools/splitter-r580/splitter.jar input/oceania_nz_ni.pbf --output-dir=work/osmsplitmaps/
