##############################################################################
#
# Generate a Garmin gmapsupp.img file from (split) OSM pbf files (map data
# and contours).  Uses style files and type rules (from txt file) in the
# generation
#
##############################################################################


# Set the name of the region being generated
region="oceania_nz_ni"

# Set the style that is to be applied when converting from OSM to Garmin
style="nonroute"

# Set the type rules that are to be applied when rendering the image file on the Garmin device
type="offroad"

# Setup paths to the input files
osm_dir="work/osmsplitmaps/${region}"
contour_dir="work/contours/${region}"

# Setup path to working files generated by this script
garmin_work_dir="work/garminsplitmaps/${region}"

# Setup path to output files
output_dir="maps/${style}/${region}"

echo "Converting OSM to Garmin for region ${region} using style ${style} and type ${type} rendering rules"

# Create directories (including parent directories) if they dont exist
mkdir -p ${garmin_work_dir}
mkdir -p ${output_dir}

# first remove any previously generated Garmin image files so as to not pollute the output
rm -f ${garmin_work_dir}/*.img

# Convert split OSM files and contours to split Garmin image files
#    - Assumes split OSM pbf files have been put in the directory osm_dir (build_split.sh does this)
#    - Assumes contour pbf files have been put in the directory work/contours (build_contours.sh does this)
echo "Converting split OSM files and contours into Garmin Image files ..."
java -Xmx1024m -jar tools/mkgmap-r3834/mkgmap.jar \
                    --remove-short-arcs \
                    --add-pois-to-areas \
                    --style-file=styles/${style}.style \
                    --precomp-sea=input/sea.zip \
                    --generate-sea \
                    --output-dir=${garmin_work_dir} \
                    ${osm_dir}/*.pbf \
                    ${contour_dir}/*.pbf

# Remove previously generated Garmin image files so as to not pollute the output
rm -f ${output_dir}/*

# Combine all the Garmin image files to a single Garmin gmapsupp image file, applying the type rules
echo "Combining Garmin Image files and applying type rules from ${type}.typ	..."
java -Xmx1024m -jar tools/mkgmap-r3834/mkgmap.jar \
                    --gmapsupp \
                    --product-id=1 \
                    --output-dir=${output_dir} \
                    ${garmin_work_dir}/*.img \
                    build/${type}.typ

#
# Build the tdb file and copy in the typ file, both required if using QLANDKARTE to view maps on the PC
#
java -jar tools/mkgmap-r3834/mkgmap.jar --tdbfile --output-dir=${output_dir}/ ${output_dir}/gmapsupp.img 
cp build/${type}.typ ${output_dir}

# Show size of resulting Garmin image file
ls -lh ${output_dir}/gmapsupp.img
