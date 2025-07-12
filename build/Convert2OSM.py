# 11-Jul-2025
# Based on example from https://github.com/roelderickx/ogr2osm

# TODO: Bounds are hard coded for now
#       Region is hardcoded as oceania_nz_ni

import logging
import ogr2osm

def convert(in_file, out_file):
  print(f"    Converting '{in_file}' to '{out_file}'...")
  # 1. Set the logging level of the logger object named 'ogr2osm' to the desired output level
  ogr2osmlogger = logging.getLogger('ogr2osm')
  ogr2osmlogger.setLevel(logging.ERROR)
  ogr2osmlogger.addHandler(logging.StreamHandler())
  
  # 2. Create the translation object. If no translation is required you
  #    can use the base class from ogr2osm, otherwise you need to instantiate
  #    a subclass of ogr2osm.TranslationBase
  translation_object = ogr2osm.TranslationBase()
  
  # 3. Create the ogr datasource. You can specify a source projection but
  #    EPSG:4326 will be assumed if none is given and if the projection of the
  #    datasource is unknown.
  datasource = ogr2osm.OgrDatasource(translation_object)
  # Optional constructor parameters:
  # - source_proj4: --proj4 parameter
  # - source_epsg: --epsg parameter
  # - gisorder: --gis-order parameter
  # - source_encoding: --encoding parameter
  datasource.open_datasource(in_file)
  # Optional open_datasource parameters:
  # - prefer_mem_copy: --no-memory-copy parameter
  
  # 4. Instantiate the ogr to osm converter class ogr2osm.OsmData and start the
  #    conversion process
  osmdata = ogr2osm.OsmData(translation_object)
  # Optional constructor parameters:
  # - rounding_digits: --rounding-digits parameter
  # - significant_digits: --significant-digits parameter
  # - max_points_in_way: --split-ways parameter
  # - add_bounds: --add-bounds parameter
  # - start_id: --id parameter
  # - is_positive: --positive-id parameter
  # - z_value_tagname: --add-z-value-tag
  osmdata.process(datasource)
  
  # 5. Instantiate either ogr2osm.OsmDataWriter or ogr2osm.PbfDataWriter and
  #    invoke output() to write the output file. If required you can write a
  #    custom datawriter class by subclassing ogr2osm.DataWriterBase.
  datawriter = ogr2osm.OsmDataWriter(out_file)
  # Optional constructor parameters:
  # - never_upload: --never-upload parameter
  # - no_upload_false: --no-upload-false parameter
  # - never_download: --never-download parameter
  # - locked: --locked parameter
  # - add_version: --add-version parameter
  # - add_timestamp: --add-timestamp parameter
  # - significant_digits: --significant-digits parameter
  # - suppress_empty_tags: --suppress-empty-tags parameter
  # - max_tag_length: --max-tag-length parameter
  osmdata.output(datawriter)
