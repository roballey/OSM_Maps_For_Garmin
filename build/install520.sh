#! /bin/sh
# Set the name of the region being generated
region="oceania_nz_ni"

# Set the style that is to be applied when converting from OSM to Garmin
style="nonroute"

# Setup path to output files
output_dir="maps/${style}/${region}"

echo "Installing map image file from ${output_dir}..."
cp ${output_dir}/gmapsupp.img /media/rob/GARMIN/Garmin/gmapbmap.img
echo "Done"
