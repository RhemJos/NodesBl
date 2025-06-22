import bpy
import sys

BLENDER_NODES_DIR = r"D:\Varios\My Path\3D Design\Blender - Orthosis\develop\NodesBl\nodes"
if BLENDER_NODES_DIR not in sys.path:
    sys.path.insert(0, BLENDER_NODES_DIR)

try:
    from base_node import RHEM_SocketTurquesaObject  
except ImportError as e:
    print(f"Error de importación: {e}")
    raise


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