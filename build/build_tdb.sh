#
# Build the tdb file and copy in the typ file both required if using QLANDKARTE to view maps on the PC
#
java -jar tools/mkgmap-r3834/mkgmap.jar --tdbfile --output-dir=maps/nonroute/ maps/nonroute/oceania_nz_ni.img 
cp build/offroad.typ maps/nonroute/offroad.typ
