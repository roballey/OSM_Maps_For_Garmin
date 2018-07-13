#
# Split single PBF file into multiple files for processing via mkgmap
#

# Set the name of the region being generated
region="oceania_nz_ni"

# Setup path to working files generated by this script
osm_work_dir="work/osmsplitmaps/${region}"

# Create directory (including parent directories) if it doesnt exist
mkdir -p ${osm_work_dir}

rm -f ${osm_work_dir}/*
java -Xmx1024m -jar tools/splitter-*/splitter.jar input/${region}.pbf --output-dir=${osm_work_dir}
