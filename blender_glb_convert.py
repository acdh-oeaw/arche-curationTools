# This script uses Blender's Python API to convert a given input file to a GLB
# It should be called with:
#   blender --background --python blender_glb_convert.py -- input.file output.glb
import bpy
import sys

# Clear default objects
bpy.ops.wm.read_factory_settings(use_empty=True)

# Get input/output paths from command line arguments
argv = sys.argv
argv = argv[argv.index("--") + 1:] # get all args after "--"
input_path = argv[0]
output_path = argv[1]

# Import PLY and Export GLB
bpy.ops.wm.ply_import(filepath=input_path)
bpy.ops.export_scene.gltf(filepath=output_path, export_format='GLB')
