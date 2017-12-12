This directory contains files to build the Garmin map images from OSM map data and SRTM height data (for contours, WIP)


Building Contours

    - Install phyghtmap
      - In linux create links from V3.X version back to V3 directory:
        - cd /usr/lib/...
        - ln -s ...
        - ln -s ...
    - Get a login at urs.earthdata.nasa.gov
    - Put earthdata login and password in build_contours.sh (actually only required the first time, after this phyghtmap caches the login)

    - Run "build_countours.sh" (will download SRTM data into "work/hgt" directory and create pbf files in "work/contours")

