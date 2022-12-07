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
   * Install phygtmap pre-reqs:
      * pip install setuptools
      * pip install matplotlib
	o pip install numpy
	o pip install beautifulsoup
	o pip install http
	o pip install cookiejar
        o pip install bs4
o Download phygtmap_2.21 from http://katze.tfiu.de/projects/phyghtmap/ and extract into /c/python27
o In /c/Python27/phyghtmap-2.21 directory run `python setup.py install`
o Edit `build/contours.py` to set your username and password for Earthexplorer

(NOTE: I'm currently, May-2019, not able to generate contours on Windows, might by a python version issue)

1. Linux:
   * Download debian package from `http://katze.tfiu.de/projects/phyghtmap/ and install
   * ...(other steps?)



### Generation Steps
----------------
1. Download an OSM extract as a PBF file and place it in the 'input' directory
1. Split the PBF file into multiple parts with 'build/split.sh'

   split.sh options:
  
     * -i=<INPUTFILE>  Specify the name of the input PBF file to split.  If not specified defaults to <REGION>.pbf
     * -p=<POLY>       Specify the name of an optional polygon file that will be used to define the region to which the split data is clipped 
     * -r=<REGION>     Specify the name of the region being split, defaults to oceania_nz_ni

1. If including contours, perform the steps from '[Generating Contours](#generating-contours)' below
1. Generate the Garmin image file with 'build/map.sh', by default this will build a routeable map without contours

   map.sh options:

     * -c    Add contour lines to map
     * -r=<REGION>  Specify the region for which map is generated, defaults to oceania_nz_ni
     * -s=<STYLE>   Use <STYLE> style rules to convert OSM data to Garmin
     * -t=<TYPE>    Use <TYPE> type rules when rendering the Garmin map


### Generating Contours
-------------------
The following steps are only required if you wish to add contour lines to the generated maps.  The steps do not need to be performed every time maps are generated as unlike OSM data the DEM data used to generate the contours does not often change.

NOTE: On Windows currently not working with Python2.7, does this require Python3?

#### Building contours from SRTM data:

Use this step to download SRTM data and build a PBF file of contours from the data.

1. Generate the contours with 'build/contours.sh'
1. Build your maps as usual using the -c option to include contours

* NOTE: Generate contours after splitting the source OSM PBF file into multiple parts as phygtmap uses the polygon file generated
during splitting to define the area extent for the contours.

#### Building contours from LINZ data:

1. Download LINZ contour data as a shapefile from https://data.linz.govt.nz/layer/50768-nz-contours-topo-150k
1. Convert LINZ contour data by loading into JOSM (requires the XXX plugin) and then saving as an OSM file
1. Split the resulting OSM file into multiple pbf files with:
        java -Xmx1000m -jar tools/splitter-*/splitter.jar [osm_file] --output-dir=work/contours/[region]
1. Build your maps as usual using the -c option to include contours

## Generating For Other regions
----------------------------
1. Download a OSM data in PBF format for the area for which you wish to generate a map.  `http://download.geofabrik.de/` is one source.  Put the file in the `input` directory
1. Create a .poly file defining the area for which you wish to generate the map.  Name the file <REGION>.poly and put it in the `input` directory.  This can be ommitted if you wish to generate for the whole downloaded area but this will probably be too big for most Garmin devices.
1. Perform the generation steps as above

See `build/nz.sh` for an example that downloads a PBF file for the whole of New Zealand and builds seperate routable and nonroutable maps for the North and South islands using two different poly files to specify the clipping area.

