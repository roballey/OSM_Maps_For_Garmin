#! /bin/sh
# Install Garmin map file on Edge 1050 mounted with MTP
# Just defaults to NZ wide routeable map for now

# Default the region and type of image to install
region="oceania_nz"
style="route"

# Destination for Garmin 1050 mounted with MTP
dest="/run/user/1000/gvfs/mtp:host=Garmin_E_0000cfbc4fce/Internal Storage/Garmin/Maps"

# Build source map directory
map_dir="maps/${style}/${region}"

echo "Installing from '${map_dir}' to '${dest}' ..."
echo "(takes ~ 15 seconds)..."
gio copy ${map_dir}/gmapsupp.img "${dest}"
echo "On Garmin:"
ls -lrth "${dest}"
