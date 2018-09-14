##############################################################################
#
# Generate a routeable Garmin gmapsupp.img file from (split) OSM pbf files
# 
# Using style and typ from OpenTopoMap to generate routable image file.
#
##############################################################################

show_help() {
  echo "Generate a Garmin image file from OSM pbf files"
  echo "Options:"
  echo "  -c  : Include contours in generated image"
  echo "  -h  : Show this help"
  echo "  -r <REGION> : Specify the region to be generated, defaults to 'oceania_nz_ni'"
  echo "  -s <STYLE> : Specify the style to be used to generate"
  echo "  -t <TYPE> : Specify the type file to be used when rendering the image"

}

# Set the name of the region being generated
region="oceania_nz_ni"

# Set the default style that is to be applied when converting from OSM to Garmin
style="route"

# Set the type rules that are to be applied when rendering the image file on the Garmin device
type="route"

tmp_dir="work/tmp"

# Default to not including contours unless over ridden on command line
contour=0

# Parse command line options
while getopts hcs:t: opt; do
    case $opt in
        h)
            show_help
            exit 0
            ;;
        c)  contour=1
            ;;
        r)  region=$OPTARG
            ;;
        s)  style=$OPTARG
            ;;
        t)  type=$OPTARG
            ;;
        *)
            show_help
            exit 1
            ;;
    esac
done

# TODO: Set the --country-name and --country-abbr passed to mkgmap if region is changed

# Setup paths to the input files
osm_dir="work/osmsplitmaps/${region}"
contour_dir="work/contours/${region}"

# Check style files exist
if [ ! -d styles/${style}.style ]
then
  echo "Style files 'styles/${style}.style' does not exist"
  exit 1
fi

# Check type file exists
if [ ! -f type/${type}.txt ]
then
  echo "Type file 'type/${type}.txt' does not exist"
  exit 1
fi

# Setup path to output files
output_dir="maps/${style}/${region}"

echo "=================================================================================================="
echo "Converting OSM to Garmin for region ${region} using style ${style} and type ${type} rendering rules"
echo "=================================================================================================="

# Create directories (including parent directories) if they dont exist
echo "Building directories"
mkdir -p ${output_dir}
mkdir -p ${tmp_dir}

# TBD: Determine if these options from OpenTopoMaps are required
# max-jobs
# latin1
# family-id=6868
# min-size-polygon=8
# polygon-size-limits=24:12, 18:10, 16:8, 14:4, 12:2, 11:0

echo "Cleaning old files"
# Remove previously generated temporary files so as to not pollute the output
rm -f ${tmp_dir}/*

# Remove previously generated Garmin image files so as to not pollute the output
rm -f ${output_dir}/*

echo "Converting type file from ${type}.txt to ${type}.typ ..."
java -Xmx1024m -jar tools/mkgmap-r*/mkgmap.jar --output-dir=type type/${type}.txt

echo "Converting split OSM files into a Garmin Image file using style ${style}.style and applying type rules from ${type}.typ ..."

if [ $contour = 1 ]
then
  echo "   Including contours..."
  inputs="${osm_dir}/*.pbf ${contour_dir}/*.pbf"
else
  echo "   No contours..."
  inputs="${osm_dir}/*.pbf"
fi

# Combine all the split OSM files to a single Garmin gmapsupp image file, using specified style and applying the type rules
java -Xmx1024m -jar tools/mkgmap-r*/mkgmap.jar \
                     --country-name="New Zealand" \
                     --country-abbr="NZ" \
                     --series-name="${type}" \
                     --family-name="OSM" \
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
                    --style-file=styles/${style}.style \
                    --precomp-sea=input/sea.zip \
                    --generate-sea \
                    --output-dir=${tmp_dir} \
                    ${inputs} \
                    type/${type}.typ

echo "Copyingoutputs into ${output_dir}"
# Move the resulting Garmin image file into the output directory
mv ${tmp_dir}/gmapsupp.img ${output_dir}

# Build the tdb file and copy in the typ file, both required if using QLANDKARTE to view maps on the PC
java -jar tools/mkgmap-r*/mkgmap.jar --tdbfile --output-dir=${output_dir}/ ${output_dir}/gmapsupp.img 
cp type/${type}.typ ${output_dir}

# Show size of resulting Garmin image file
ls -lh ${output_dir}/gmapsupp.img
