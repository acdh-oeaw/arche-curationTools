#!/bin/bash
# Script assuring TIF files in a given directory
# (passed as a first parameter or a current working dir otherwise)
# are LZW-compressed.
#
# Uses gdal_translate for the LZW compression and then copies
# image metadata using the exiftool
if [ "$1" != "" ] ; then
    cd "$1"
fi
echo "Processing directory `pwd`"
for F in `ls -1 | grep -i -E 'tiff?$'` ; do
    gdalinfo "$F" | grep -q 'COMPRESSION=LZW'
    FLAG_NC="$?"
    FLAG_T=`gdalinfo "$F" | grep -E 'Block=[0-9]+x1 ' | wc -l`
    if [ "$FLAG_NC" != "0" ] || [ "$FLAG_T" != "0" ] ; then
        echo "  Compressing $F"
        FTMP="__tmp__$F"
        gdal_translate -co "COMPRESS=LZW" -co "PREDICTOR=2" -co "TILED=YES" "$F" "$FTMP" 2>&1 > /dev/null &&\
        exiftool -m -overwrite_original_in_place -tagsFromFile "$F" "$FTMP" 2>&1 > /dev/null &&\
        mv "$FTMP" "$F"
        if [ "$?" != "0" ] ; then
            echo "    failed"
        fi
	rm -f "$FTMP"
    fi
done
