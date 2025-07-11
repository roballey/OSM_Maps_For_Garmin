#! /bin/sh
##############################################################################
#
# Generate a routeable Garmin gmapsupp.img file from (split) OSM pbf files
# 
# TODO: Make downloading and splitting part of this script for osm and mapillary files
# TODO: Download OSM notes as part of this script
##############################################################################

show_help() {
  echo "Generate a Garmin image file from OSM pbf files"
  echo "Options:"
  echo "  -c  : Include contours in generated image"
  echo "  -m  : Include Mapillary coverage in generated image"
  echo "  -n  : Include OSM notes in generated image"
  echo "  -h  : Show this help"
  echo "  -r <REGION> : Specify the region to be generated, defaults to 'oceania_nz'"
  echo "  -s <STYLE> : Specify the style to be used to generate, defaults to 'route'"
  echo "  -t <TYPE> : Specify the type file to be used when rendering the image, defaults to 'route'"
}

mem="8000m"

# FIXME: Replace region with <CONTINENT>, <COUNTRY> and optional <REGION>.  
#        Put output files in a hierarchical directory structure
#        Set the --country-name and --country-abbr passed to mkgmap based on <COUNTRY>

# Set defaults (can be overridden with command line arguments)
region="oceania_nz"
style="route"
type="route"
contour=0
mapillary=0
notes=0

# Parse command line options
while getopts hcmnr:s:t: opt; do
    case $opt in
        h)
            show_help
            exit 0
            ;;
        c)  contour=1
            ;;
        m)  mapillary=1
            ;;
        n)  notes=1
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

# Setup path to working directory
tmp_dir="work/tmp"

# Setup paths to the input files
input_osm_dir="work/osmsplitmaps/${region}"
input_contour_dir="work/contours/${region}"
input_mapillary_dir="downloads/mapillary/${region}"
input_notes_dir="downloads/notes/${region}"

# Setup path to output files
output_dir="maps/${style}/${region}"

echo "--------------------------------------------------------------------------------------------------"
echo "--------------------------------------------------------------------------------------------------"
echo "Converting OSM to Garmin for region ${region} using style ${style} and type ${type} rendering rules"
if [ $contour = 1 ]
then
  echo "   +++ Including contours..."
else
  echo "   --- No contours..."
fi

if [ $mapillary = 1 ]
then
  echo "   +++ Including Mapillary coverage..."
else
  echo "   --- No Mapillary coverage..."
fi

if [ $notes = 1 ]
then
  echo "   +++ Including notes markers..."
else
  echo "   --- No notes markers..."
fi

# Check style files exist
if [ ! -d styles/${style}.style ]
then
  echo "--------------------------------------------------------------------------------------------------"
  echo "Style files directory 'styles/${style}.style' does not exist"
  exit 1
fi

# Check type file exists
if [ ! -f type/${type}.txt ]
then
  echo "--------------------------------------------------------------------------------------------------"
  echo "Type file 'type/${type}.txt' does not exist"
  exit 1
fi

version=`date +%y%m`

if [ $contour = 1 ]
then
  echo "--------------------------------------------------------------------------------------------------"
  echo "Setting contour inputs"

  if [ ! -d ${input_contour_dir} ]
  then
    echo "Contour files directory '${input_contour_dir}' does not exist"
    exit 1
  fi
  inputs="${input_osm_dir}/*.pbf ${input_contour_dir}/*.pbf"
  output_img="${output_dir}/gmapsupp_contours.img"
else
  inputs="${input_osm_dir}/*.pbf"
  output_img="${output_dir}/gmapsupp.img"
fi

if [ $mapillary = 1 ]
then
  echo "--------------------------------------------------------------------------------------------------"
  echo "Setting Mapillary inputs"

  if [ ! -d ${input_mapillary_dir} ]
  then
    echo "Mapillary files directory '${input_mapillary_dir}' does not exist"
    exit 1
  fi
  inputs="${inputs} ${input_mapillary_dir}/sequences.osm"
fi

if [ $notes = 1 ]
then
  echo "--------------------------------------------------------------------------------------------------"
  echo "Setting OSM notes inputs"

  if [ ! -d ${input_notes_dir} ]
  then
    echo "OSM Notes files directory '${input_notes_dir}' does not exist"
    exit 1
  fi
  inputs="${inputs} ${input_notes_dir}/notes.osm"
fi

# Create output and temp directories (including parent directories) if they dont exist
echo "--------------------------------------------------------------------------------------------------"
echo "Building directories"
mkdir -p ${output_dir}
mkdir -p ${tmp_dir}

echo "--------------------------------------------------------------------------------------------------"
echo "Cleaning old files"
# Remove previously generated temporary files so as to not pollute the output
rm -f ${tmp_dir}/*

# Remove previously generated Garmin image files so as to not pollute the output
rm -f ${output_img}
rm -f ${output_dir}/${type}.typ
rm -f ${output_dir}/*.tdb

echo "--------------------------------------------------------------------------------------------------"
echo "Converting type file from ${type}.txt to ${type}.typ ..."
java -Xmx${mem} -jar tools/mkgmap-r*/mkgmap.jar --output-dir=${tmp_dir} type/${type}.txt

echo "--------------------------------------------------------------------------------------------------"
echo "Converting split OSM files into a Garmin Image file:"
echo "  Inputs from '${inputs}'"
echo "  Using style ${style}.style"
echo "  Applying type rules from ${type}.typ ..."
# Combine all the split OSM files and other inputs to a single Garmin gmapsupp image file, using specified style and applying the type rules
java -Xmx${mem} -jar tools/mkgmap-r*/mkgmap.jar \
                    --family-name="OSM for Garmin" \
                    --series-name="${type}" \
		    --description="OSM maps for Garmin devices" \
		    --product-version=$version \
		    --region-name="Oceania" \
                    --country-name="New Zealand" \
                    --country-abbr="NZ" \
		    --drive-on=left \
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
                    --precomp-sea=downloads/sea-latest.zip \
                    --generate-sea \
                    --output-dir=${tmp_dir} \
                    ${inputs} \
                    ${tmp_dir}/${type}.typ

echo "--------------------------------------------------------------------------------------------------"
echo "Moving output image files from ${tmp_dir} into ${output_dir}"
# Move the resulting Garmin image file into the output directory
mv ${tmp_dir}/gmapsupp.img ${output_img}

# Show size of resulting Garmin image file
ls -lh ${output_img}

echo "Image file is '${output_img}' version ${version}"
