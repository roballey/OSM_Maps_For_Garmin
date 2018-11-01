#! /bin/sh
# Set the name of the region being generated
region="oceania_nz_ni"

# Set the style that is to be applied when converting from OSM to Garmin
style="route"

# Setup path to output files
output_dir="maps/${style}/${region}"

cp ${output_dir}/gmapsupp.img /media/rob/92E4-4983/GARMIN/gmapsupp.img
