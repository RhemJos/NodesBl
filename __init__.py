import os
import sys
import bpy
from nodeitems_utils import NodeCategory, NodeItem, register_node_categories, unregister_node_categories

# Path:
BLENDER_NODES_DIR = r"D:\Varios\My Path\3D Design\Blender - Orthosis\develop\NodesBl"
if BLENDER_NODES_DIR not in sys.path:
    sys.path.insert(0, BLENDER_NODES_DIR)

try:
    from base_node import (RhemWorkflowNodeTree, RHEM_SocketAzulFloat, RHEM_SocketTurquesaObject,
                           RHEM_SocketNaranjaInt,)
    from input_nodes import NodoEntradaObjeto
except ImportError as e:
    print(f"Error de importación: {e}")
    raise

# Classes to register:
node_classes = [
    RhemWorkflowNodeTree,
    RHEM_SocketAzulFloat,
    RHEM_SocketTurquesaObject,
    RHEM_SocketNaranjaInt,
    NodoEntradaObjeto,
    # NodoDisplace,
    # NodoRhemRemesh,
]

# Node categories
node_categories = [
    NodeCategory("RHEM_NODE", "Rhem Organized Nodes", items=[
        NodeItem("NodoEntradaObjetoType"),
        # NodeItem("NodoDisplaceType"),
        # NodeItem("NodoRhemRemeshType"),
    ]),
]

def register():
    try:
        for node_class in node_classes:
            if hasattr(bpy.types, node_class.__name__):
                bpy.utils.unregister_class(node_class)
                print(f"(Re)registrando clase: {node_class.__name__}")
            bpy.utils.register_class(node_class)
        register_node_categories("RHEM_NODE", node_categories)
        print("¡Nodos registrados correctamente en Blender!")
    except Exception as e:
        print(f"Error al registrar nodo: {e}")

def unregister():
    try:
        unregister_node_categories("RHEM_NODE")
    except Exception as e:
        print(f"Categoría ya desregistrada o no registrada: {e}")

    for cls in reversed(node_classes):
        try:
            bpy.utils.unregister_class(cls)
        except Exception as e:
            print(f"No se pudo desregistrar {cls.__name__}: {e}")
    print("¡Nodos DESregistrados correctamente!")

if __name__ == "__main__":
    print("################################################################################")
    try:
        unregister()
    except Exception as e:
        print(f"Error al desregistrar: {e}")
    register()