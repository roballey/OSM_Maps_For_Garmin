#! /bin/sh

# Like nz.sh but just builds a small test area

# Split input file, for test area
# NOTE: Commented out to speed it up
#echo "Splitting ..."
#build/split.sh -r test -p test.poly -i oceania_nz.pbf

# Build Garmin img file from split PBFs
echo "Building test image file style=route type=route ..."
build/map.sh -t route -s route -r test

# Rename resulting image file so it's easier to distnguish in QMapShack
mv maps/route/test/gmapsupp.img maps/route/test/test.img
echo "Test image file is 'maps/route/test/test.img'"
