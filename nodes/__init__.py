import bpy
from nodeitems_utils import NodeCategory, NodeItem
from .base_node import (
    RhemWorkflowNodeTree,
    RHEM_SocketAzulFloat,
    RHEM_SocketTurquesaObject,
    RHEM_SocketNaranjaInt
)

from .input_nodes import NodoEntradaObjeto
from .modify_nodes import NodoDisplace
from .remesh_nodes import NodoRhemRemesh

# Lista de clases para registrar
node_classes = [
    RhemWorkflowNodeTree,
    RHEM_SocketAzulFloat,
    RHEM_SocketTurquesaObject,
    RHEM_SocketNaranjaInt,
    NodoEntradaObjeto,
    NodoDisplace,
    NodoRhemRemesh,
]

# Categorías de nodos
node_categories = [
    NodeCategory("RHEM_NODE", "Rhem Organized Nodes", items=[
        NodeItem("NodoEntradaObjetoType"),
        NodeItem("NodoDisplaceType"),
        NodeItem("NodoRhemRemeshType"),
    ]),
]

def register_nodes():
    from nodeitems_utils import register_node_categories
    from bpy.utils import register_class
    
    for cls in node_classes:
        register_class(cls)
    
    register_node_categories("RHEM_NODE", node_categories)

def unregister_nodes():
    from nodeitems_utils import unregister_node_categories
    from bpy.utils import unregister_class
    
    unregister_node_categories("RHEM_NODE")
    
    for cls in reversed(node_classes):
        unregister_class(cls)