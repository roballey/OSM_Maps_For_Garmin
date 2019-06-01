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

Only if you want to include contours built from SRTM data:

1. Windows
o Install phygtmap pre-reqs:
	o pip install setuptools
	o pip install matplotlib
	o pip install numpy
	o pip install beautifulsoup
	o pip install http
	o pip install cookiejar
        o pip install bs4
o Download phygtmap_2.21 from http://katze.tfiu.de/projects/phyghtmap/ and extract into /c/python27
o In /c/Python27/phyghtmap-2.21 directory run `python setup.py install`
o Edit `build/contours.py` to set your username and password for Earthexplorer

(NOTE: I'm currently, May-2019, not able to generate contours on Windows, might by a python version issue)

1. Linux
TBD


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

NOTE: On Windows currently not working with Python2.7, does this require Python3?

#### Building contours from SRTM data:

Use this step to download SRTM data and build a PBF file of contours from the data.

1. Generate the contours with 'build/contours.sh'
1. Build you maps as usual using the -c option to include contours

* NOTE: Generate contours after splitting the source OSM PBF file into multiple parts as phygtmap uses the polygon file generated
during splitting to define the area extent for the contours.

#### Building contours from LINZ data:

1. Download LINZ contour data as a shapefile from https://data.linz.govt.nz/layer/50768-nz-contours-topo-150k
1. Convert LINZ contour data by loading into JOSM (requires the XXX) plugin and then saving as an OSM file
1. Split the resulting OSM file into multiple pbf files with:
        java -Xmx1000m -jar tools/splitter-*/splitter.jar [osm_file] --output-dir=work/contours/[region]
1. Build you maps as usual using the -c option to include contours

## Generating For Other regions
----------------------------
TBD

