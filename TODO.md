In Progress:
   - Differentiate between service and residential roads on Garmin (see Changes.xlsx)

Todo:

   - Look at modifying scripts to use external `getopt` instead of built-in getopts for parsing (and use long options).  
      - See:
        - https://gist.github.com/cosimo/3760587 
        - https://www.mkssoftware.com/docs/man1/getopt.1.asp
   - Combine split.sh into map.sh, make splitting optional based on command line arguments
   - Change poi, polygon and line indexes to match Garmin standard indexes as per https://wiki.openstreetmap.org/wiki/GroundTruth_Standard_Garmin_Types
   - See also https://wiki.openstreetmap.org/wiki/OSM_Map_On_Garmin/POI_Types for type codes
   - Change draw order to match polygon changes above.

   Typ file:
      - Improve waterfall icon (make bolder)
      - Make contour lines less prominent

Done:   
   - Improve detection of closed tracks/paths
   - Remove unused items from type file
   - Add contours 
   - Put work and output files in sub directories based on a region name
   - Change build*.sh scripts to be proper scripts that accept arguments etc.
   - Render man_made=footwear_decontamination
   - Improve name of maps (Now appears as "OSM For Garmin" in settings/maps on Edge705)
   - Add a script to download the source data from geofabrik
