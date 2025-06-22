import bpy

class RHEM_OT_Remesh(bpy.types.Operator):
    bl_idname = "rhem.remesh"
    bl_label = "Aplicar Remesh"
    
    nodo_idname: bpy.props.StringProperty()

    def execute(self, context):
        espacio = context.space_data
        arbol = espacio.node_tree
        print("Ejecuto")

        if not arbol:
            self.report({'ERROR'}, "No hay árbol de nodos activo.")
            return {'CANCELLED'}
        print("Arbol")
        nodo = arbol.nodes.get(self.nodo_idname)
        if nodo and hasattr(nodo, "process"):
            nodo.process()
            print("Listo")
            return {'FINISHED'}
        else:
            self.report({'ERROR'}, "No se encontró el nodo o el método.")
            return {'CANCELLED'}


operator_classes = [
    RHEM_OT_Remesh,
]

def register_operators():
    from bpy.utils import register_class
    
    for cls in operator_classes:
        register_class(cls)

def unregister_operators():
    from bpy.utils import unregister_class
    
    for cls in reversed(operator_classes):
        unregister_class(cls)