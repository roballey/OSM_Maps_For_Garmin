#! /bin/sh
input_file="test/test.osm"
type_txtfile="type/route.txt"
root_dir="test"
split_dir="${root_dir}/split"
tmp_dir="${root_dir}/tmp"
work_dir="${root_dir}/work"
image_file="test_route.img"

# Split input file
echo "========================================================================================"
echo "=== TEST: Splitting ${input_file} ..."
java -Xmx1000m -jar tools/splitter-*/splitter.jar $input_file --output-dir=${split_dir}

echo "========================================================================================"
echo "=== TEST: Generating type file from txt ${type_txtfile} ..."
java -Xmx1000m -jar tools/mkgmap-r*/mkgmap.jar --output-dir=${work_dir} $type_txtfile
echo
echo "========================================================================================"
version=`date +%y%m`
echo "=== TEST: Setting version number to ${version}..."

# Build Garmin img files from split files
echo "========================================================================================"
echo "=== TEST: Building image file ..."
java -Xmx1000m -jar tools/mkgmap-r*/mkgmap.jar \
                    --family-name="Test OSM for Garmin" \
                    --series-name="Route" \
		    --description="Test OSM maps for Garmin devices" \
		    --product-version=$version \
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
                    --output-dir=${tmp_dir} \
		    ${split_dir}/*.pbf \
                    ${work_dir}/route.typ

echo "========================================================================================"
echo "=== TEST: Moving image file ${image_file} ..."
mv ${tmp_dir}/gmapsupp.img test/maps/${image_file}

echo "========================================================================================"
echo "=== TEST: Map version is $version"
