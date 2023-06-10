This directory contains files for testing generation of Garmin img files.

test.sh - Builds a test_route.img file under test/amps from test/test.osm file
          using types and styles for rotable maps from directories used by ../build/map.sh

install705-1/sh - Install test_route.img file as gmapsupp.img on Garmin 705 for testing

test.osm - Input file from which to generate map (not configured in git) - save this from JOSM

Viewing:
Setup QMapShack to use generated map (If already running, reload maps then activate test_route) and/or
Install on Garmin 705 with install script
