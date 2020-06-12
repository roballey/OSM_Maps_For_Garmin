#! /bin/sh
# Default the region and type of image to install
region="oceania_nz_ni"
style="route"
output_dir="maps/${style}/${region}"

# Copy to supplementary map file on Garmin SD-Card of Edge 705-1
cp ${output_dir}/gmapsupp.img /media/rob/92E4-4983/GARMIN/gmapsupp.img
