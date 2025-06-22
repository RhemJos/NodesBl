import bpy
from .base_node import RHEM_SocketTurquesaObject

class NodoEntradaObjeto(bpy.types.Node):
    bl_idname = "NodoEntradaObjetoType"
    bl_label = "Entrada Objeto"
    bl_icon = "OBJECT_DATA"

    objeto_nombre: bpy.props.StringProperty(name="Objeto")

    def init(self, context):
        self.outputs.new("RHEM_SocketTurquesaObject", "Objeto Rhem").prop_name = "objeto_nombre"

    def draw_buttons(self, context, layout):
        layout.prop_search(self, "objeto_nombre", context.scene, "objects", text="Objeto")

    def process(self):
        if self.objeto_nombre in bpy.data.objects:
            return bpy.data.objects[self.objeto_nombre]
        return None
