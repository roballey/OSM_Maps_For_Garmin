# OSM_Maps_For_Garmin
Maps for Garmin GPS units generated from OpenStreetMap data using mkgmap.  Includes all the configuration files used to generate the Garmin maps

##Using Pre-Generated Maps
------------------------
The directories maps/nonroute/oceania_nz_ni and maps/route/oceania_nz_ni contain gmapsupp.img files for non-routeable and routable maps of the New Zealand North Island respectively.  These image files can be installed and used on a Garmin device.

##Generating Your Own Maps
------------------------

The following instructions work under Linux or Windows if running a Bourne shell compatible shell (e.g. bash under Cygwin or Mingw/Msys etc.)

As described below these steps will generate maps for the New Zealand North Island, generating for other regions involves editing the scripts as described later in this document.

###Setup steps
-----------
The following setup steps only need to be performed once:

i) Download splitter from http://www.mkgmap.org.uk/download/splitter.html and install in 'tools'
ii) Download mkgmap from http://www.mkgmap.org.uk/download/mkgmap.html and install in 'tools'
iii) Download sea.zip from http://www.mkgmap.org.uk/download/splitter.html and install in 'input'

###Contour Steps
-------------
The following steps are only required if you wish to add contour lines to the generated maps.  The steps do not need to be performed everytime maps are generated as unlike OSM data the DEM data used to generate the contours does not often change.

####Building contours from SRTM data:

i) TBD

####Building contours from LINZ data:

i) TBD

###Generation Steps
----------------
1) Download an OSM extract as a PBF file and place it in the input directory
2) Split the PBF file into multiple parts with 'build/split.sh'
3) Generate the Garmin image file with 'build/map.sh', by default this will build a routeable map without contours

   map.sh options:

     -c    Add contour lines to map
     -s=<STYLE>   Use <STYLE> style rules to convert OSM data to Garmin
     -t=<TYPE>    Use <TYPE> type rules when rendering the Garmin map


##Generating For Other regions
----------------------------
