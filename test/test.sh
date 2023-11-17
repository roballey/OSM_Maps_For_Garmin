#! /bin/sh
version_file="test/map_version.txt"

# Split input file
echo "========================================================================================"
echo "=== TEST: Splitting ..."
java -Xmx1000m -jar tools/splitter-*/splitter.jar test/test.osm --output-dir=test/split

echo "========================================================================================"
echo "=== TEST: Generating type file from txt ..."
java -Xmx1000m -jar tools/mkgmap-r*/mkgmap.jar --output-dir=test/work type/route.txt

echo "========================================================================================"
echo "=== TEST: Incrementing version number ..."
awk '{$1=$1+1}'1 ${version_file} >test/tmp.txt && mv test/tmp.txt ${version_file}

# Build Garmin img files from split files
echo "========================================================================================"
echo "=== TEST: Building image file ..."
java -Xmx1000m -jar tools/mkgmap-r*/mkgmap.jar \
                    --family-name="Test OSM for Garmin" \
                    --series-name="Route" \
		    --description="Test OSM maps for Garmin devices" \
		    --product-version=`cat ${version_file}` \
		    --region-name="Oceania" \
                    --country-name="New Zealand" \
                    --country-abbr="NZ" \
                    --index \
                    --housenumbers \
                    --route \
                    --adjust-turn-headings \
                    --add-pois-to-areas \
                    --make-opposite-cycleways \
                    --link-pois-to-ways \
                    --process-destination \
                    --process-exits \
                    --remove-short-arcs \
                    --gmapsupp \
                    --product-id=1 \
                    --style-file=styles/route.style \
                    --precomp-sea=input/sea.zip \
                    --generate-sea \
                    --output-dir=test/tmp \
                    test/split/*.pbf \
                    test/work/route.typ

echo "========================================================================================"
echo "=== TEST: Moving image file ..."
mv test/tmp/gmapsupp.img test/maps/test_route.img

echo "========================================================================================"
echo "=== TEST: Map version is "`cat ${version_file}`
