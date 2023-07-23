#! /bin/sh
# Default the region and type of image to install
region="oceania_nz_ni"
style="route"
output_dir="maps/${style}/${region}"

# Copy to supplementary map file on Garmin SD-Card of Edge 705-1
#cp ${output_dir}/gmapsupp.img /media/rob/92E4-4983/GARMIN/gmapsupp.img
# Updated to list file sizes and use Acer Aspire 5 Linut Mint mount point
echo "Installing ${output_dir} ..."
echo "Before " `ls -lh /media/rob/HOCO64/Garmin/gmapsupp.img`
cp ${output_dir}/gmapsupp.img /media/rob/HOCO64/Garmin/gmapsupp.img
echo "After " `ls -lh /media/rob/HOCO64/Garmin/gmapsupp.img`

