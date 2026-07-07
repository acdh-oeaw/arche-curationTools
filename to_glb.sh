#!/bin/bash
# Script converting files to GLB by using the blender_glb_convert.py
#
# Uses the blender_glb_convert.py which uses the Blender
#
# Can be used on known paths, e.g.:
#  ./to_glb.sh some/path.ply other/path.ply
# or combined with the find, e.g.:
#   find /some/dir -type f -name '*ply' -exec to_glb.sh {} \;
#
# The script doesn't remove the original files.
#
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
for i in "$@" ; do
    echo "Converting $i"
    blender --background --python "$SCRIPT_DIR/blender_glb_convert.py" -- "$i" tmp.glb && \
        mv tmp.glb "${i%.*}.glb"
done
