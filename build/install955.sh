#! /bin/sh
# Install Garmin map file on 955 mounted with MTP
# Just defaults to NZ wide routeable map for now
# FIXME: ls -lh reports size of 0, seems ok in Nautilus file explorer

# Default the region and type of image to install
region="oceania_nz"
style="route"

# Destination for Garmin 955 mounted with MTP
dest="/run/user/1000/gvfs/mtp:host=091e_4fb8_0000cbd4bc05/Internal Storage/GARMIN/nzroute.img"

# Build source map directory
map_dir="maps/${style}/${region}"

echo "Installing ${map_dir} to ${dest} ..."
echo "(takes ~ 15 seconds)..."
gio copy ${map_dir}/gmapsupp.img "${dest}"
echo "On Garmin:"
ls -lh "${dest}"
echo "(Size reports as 0 for some reason)"
