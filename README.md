# OSM_Maps_For_Garmin
Maps for Garmin GPS units generated from OpenStreetMap data using mkgmap.  Includes all the configuration files used to generate the Garmin maps

## Using Pre-Generated Maps
------------------------
The directories maps/nonroute/oceania_nz_ni and maps/route/oceania_nz_ni contain gmapsupp.img files for non-routeable and routable maps of the New Zealand North Island respectively.  These image files can be installed and used on a Garmin device.

## Generating Your Own Maps
------------------------

The following instructions work under Linux or Windows if running a Bourne shell compatible shell (e.g. bash under Cygwin or Mingw/Msys etc.)

As described below these steps will generate maps for the New Zealand North Island, generating for other regions involves editing the scripts as described later in this document.

### Setup steps
-----------
The following setup steps only need to be performed once:

1. Download splitter from http://www.mkgmap.org.uk/download/splitter.html and install in 'tools'
1. Download mkgmap from http://www.mkgmap.org.uk/download/mkgmap.html and install in 'tools'
1. Download sea.zip from http://www.mkgmap.org.uk/download/splitter.html and install in 'input'

Only if you want to include contours:

1. Download phyghtmap from http://katze.tfiu.de/projects/phyghtmap/ and install in 'tools'

### Generation Steps
----------------
1. Download an OSM extract as a PBF file and place it in the 'input' directory
1. Split the PBF file into multiple parts with 'build/split.sh'
1. If including contours, perform the steps from '[Generating Contours](#generating-contours)' below
1. Generate the Garmin image file with 'build/map.sh', by default this will build a routeable map without contours

   map.sh options:

     * -c    Add contour lines to map
     * -s=<STYLE>   Use <STYLE> style rules to convert OSM data to Garmin
     * -t=<TYPE>    Use <TYPE> type rules when rendering the Garmin map


### Generating Contours
-------------------
The following steps are only required if you wish to add contour lines to the generated maps.  The steps do not need to be performed every time maps are generated as unlike OSM data the DEM data used to generate the contours does not often change.

#### Building contours from SRTM data:

Use this step to download SRTM data and build a PBF file of contours from the data.

1. Generate the contours with 'build/contours.sh'

* TBD: Does contours.sh need to be modified to allow specifying earthexplorer username and password?
* NOTE: Generate contours after splitting the source OSM PBF file into multiple parts as phygtmap uses the polygon file generated
during splitting to define the area extent for the contours.

#### Building contours from LINZ data:

1. Download LINZ contour data (TBD: Where? How?)
1. Convert LINZ contour data (TBD: How?)
1. Generate the contours with 'build/contours.sh'

## Generating For Other regions
----------------------------
TBD

