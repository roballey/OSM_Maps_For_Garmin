#
# Split single PBF file into multiple files for processing via mkgmap
#
java -Xmx1024m -jar tools/splitter-r580/splitter.jar input/oceania_nz_ni.pbf --output-dir=work/osmsplitmaps/