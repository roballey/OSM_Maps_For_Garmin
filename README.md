# OSM_Maps_For_Garmin
Maps for Garmin GPS units generated from OpenStreetMap data using mkgmap.  Includes all the configuration files used to generate the Garmin maps

## Using Pre-Generated Maps
------------------------
See the release zip files for routable and non-routable maps of the whole of NZ and the North Island and South Island seperately.

## Generating Your Own Maps
------------------------

The following instructions work under Linux

### Setup steps
-----------
The following setup steps only need to be performed once:

1. Download splitter from http://www.mkgmap.org.uk/download/splitter.html and install in 'tools'
1. Download mkgmap from http://www.mkgmap.org.uk/download/mkgmap.html and install in 'tools'
1. ~~Download sea.zip from http://www.mkgmap.org.uk/download/ and install in 'input' named 'sea-latest.zip'~~ (No longer from mkgmap.org in 2025, see below)
2. Download a `sea*.zip` file from https://thkukuk.de/osm/data/ or http://develop.freizeitkarte-osm.de/boundaries/ and install in 'input' named 'sea-latest.zip'

### Generating Maps for existing supported regions
-----------------------

The existing configurations found in the `config` directory may be specified ...

### Generating Maps for new regions
-----------------------

Create a configuration file and execute `Build.py` specifying the config file.

## Build.py usage
-----------------------
Build.py in the build directory is a python script to automate building Garmin image files.  Optionally, as well as the OSM map data, it can include:

1.  Mapillary coverage data (experimental)
1.  OSM notes
1.  Contours

### Config file

A config file specifies at a minimum the data to be downloaded; the variants (style and type) to be built and the regions to be built.  The config file must always be specified on the command line.  See the `config` directory for examples.  config file format documentation is TBD

### Options

The following options may be specified on the command line:

#### Download Control

The download control options are handy when experimenting and allow different configurations and options to be exeprimented with without continually downloading data (which is slow and stresses the servers that provide the data)
instead data previously downloaded will be used if available

o  -nd | --no-download   : Don't download anything
o  -ndo | --no-download-osm : Don't download OSM map data
o  -ndm | --no-download-mapillary : Don't download Mapillary data

#### Splitting Control

o  -ns | --no-split : Don't split the donwloaded OSM map data

#### Build Control

o  -nb | --no-build : Don't build the Garmin IMG file map

#### Extra Data

As well as the OSM Map data the generated Garmin IMG file map may also include optional extra data:

o  -c | --contours : Include contours in the map
o  -m | --mapillary : Include Mapillary coverage in the map (Experimental)
o  -n | --notes : Include OSM notes in the map


## Previewing Garmin maps on PC
-----------------------
Under either Linux or Windows `QMapShack` may be installed and used to preview the Garmin map img files
