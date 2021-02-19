#! /bin/sh
echo "*************************************************************************************************"
echo "FIXME: For some reason copying file via this script or direct cp command fails (unit disconnects)"
echo "       with the card in the GPS.  Insert card into PC directly and manually copy instead"
echo "*************************************************************************************************"

show_help() {
  echo "Install supplamentary map image file on Garmin GPS device"
  echo "Options:"
  echo "  -h  : Show this help"
  echo "  -r <REGION> : Specify the region image to be installed, defaults to 'oceania_nz'"
}

# Default the region and type of image to install
region="oceania_nz"
style="route"

# Destination file on this device
dest="/media/rob/705-2/Garmin/gmapsupp.img"

# Parse command line options
while getopts hr: opt; do
    case $opt in
        h)
            show_help
            exit 0
            ;;
        r)  region=$OPTARG
            ;;
        *)
            show_help
            exit 1
            ;;
    esac
done

output_dir="maps/${style}/${region}"

# Copy to supplementary map file on SD-Card of Garmin GPS device
echo "Installing ${output_dir} ..."
cp ${output_dir}/gmapsupp.img ${dest}
ls -lh ${dest}
