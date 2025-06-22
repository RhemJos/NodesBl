import os
import sys
import bpy

# Configuración de paths - VERIFICA ESTA RUTA
BLENDER_NODES_DIR = r"D:\Varios\My Path\3D Design\Blender - Orthosis\develop\NodesBl\nodes"
if BLENDER_NODES_DIR not in sys.path:
    sys.path.insert(0, BLENDER_NODES_DIR)

# Debug: Verificar contenido del directorio
print("\nContenido del directorio nodes:")
try:
    print(os.listdir(BLENDER_NODES_DIR))
except Exception as e:
    print(f"Error al listar directorio: {e}")

# Importación CORREGIDA (sin 'nodes.')
try:
    from base_node import RhemWorkflowNodeTree  # <-- Cambio crucial aquí
    print("¡Importación exitosa!")
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