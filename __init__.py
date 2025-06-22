import os
import sys
import bpy

# Path:
BLENDER_NODES_DIR = r"D:\Varios\My Path\3D Design\Blender - Orthosis\develop\NodesBl\nodes"
if BLENDER_NODES_DIR not in sys.path:
    sys.path.insert(0, BLENDER_NODES_DIR)

try:
    from base_node import RhemWorkflowNodeTree  
except ImportError as e:
    print(f"Error de importación: {e}")
    raise



def register():
    try:
        bpy.utils.register_class(RhemWorkflowNodeTree)
        print("¡Nodo registrado correctamente en Blender!")
    except Exception as e:
        print(f"Error al registrar nodo: {e}")

register()