#! /bin/sh
# Default the region and type of image to install
region="oceania_nz_ni"
style="route"
output_dir="maps/${style}/${region}"

# Copy to supplementary map file on Garmin SD-Card of Edge 705-2
cp ${output_dir}/gmapsupp.img /media/rob/6164-3234/GARMIN/gmapsupp.img
