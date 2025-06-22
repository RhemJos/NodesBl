import bpy
import importlib
import sys
for name, text in bpy.data.texts.items():
    if name.endswith('.py') and name[:-3] not in sys.modules:
        sys.modules[name[:-3]] = text.as_module()
from nodes import register_nodes, unregister_nodes
from operators import register_operators, unregister_operators

bl_info = {
    "name": "Rhem Nodes",
    "author": "Rhem",
    "version": (1, 0),
    "blender": (4, 0, 0),
    "location": "Node Editor",
    "description": "Nodos personalizados para el flujo de trabajo Rhem",
    "warning": "",
    "category": "Node",
}

def recargar_modulos():
    modulos = [
        'base_node',
        'input_nodes',
        'modify_nodes',
        'remesh_nodes',
        'operators'
    ]
    
    for mod in modulos:
        if mod in sys.modules:
            importlib.reload(sys.modules[mod])

def register():
    recargar_modulos()
    register_nodes()
    register_operators()

def unregister():
    unregister_nodes()
    unregister_operators()

if __name__ == "__main__":
    try:
        unregister()
    except:
        pass
    register()