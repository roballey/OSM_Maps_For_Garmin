#! /bin/sh
# Install Garmin map file to SD Card for Garmin 705-2
# Installation over USB direct connection no longer works (map file too big?)

show_help() {
  echo "Install supplamentary map image file on Garmin GPS device"
  echo "Options:"
  echo "  -h  : Show this help"
  echo "  -r <REGION> : Specify the region image to be installed, defaults to 'oceania_nz'"
}

# Default the region and type of image to install
region="oceania_nz"
style="route"

# Destination file on this device - assumes SD Card is mounted
dest="/media/rob/HOCO64/Garmin/gmapsupp.img"

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

map_dir="maps/${style}/${region}"

# Copy to supplementary map file on SD-Card
echo "Installing ${map_dir} to ${dest} ..."
cp ${map_dir}/gmapsupp.img ${dest}
ls -lh ${dest}
