#! /bin/sh
# Install Garmin map file on 965 mounted with MTP
# Just defaults to NZ wide routeable map for now

# Default the region and type of image to install
region="oceania/nz"
style="route"

# Destination for Garmin 965 mounted with MTP
dest="/run/user/1000/gvfs/mtp:host=091e_50db_0000d8dc91f9/Internal Storage/GARMIN/nzroute.img"

# Build source map directory
map_dir="maps/${style}/${region}"

echo "Installing from '${map_dir}' to '${dest}' ..."
echo "(takes ~ 15 seconds)..."
gio copy ${map_dir}/gmapsupp.img "${dest}"
echo "On Garmin:"
ls -lh "${dest}"
