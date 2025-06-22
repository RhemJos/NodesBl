import bpy
from nodeitems_utils import NodeCategory, NodeItem

class RhemWorkflowNodeTree(bpy.types.NodeTree):
    '''Custom Node Tree Type'''
    bl_idname = "RhemWfNodeTreeType"
    bl_label = "Rhem Workflow"
    bl_icon = "NODETREE"
    
    def process(self):
        for node in self.nodes:
            if hasattr(node, "process"):
                node.process()

# Custom Sockets:
class RHEM_SocketAzulFloat(bpy.types.NodeSocket):
    bl_idname = "RHEM_SocketAzulFloat"
    bl_label = "Socket Azul Float"
    
    prop_name: bpy.props.StringProperty(default="valor_float")

    def draw(self, context, layout, node, text):
        if hasattr(node, self.prop_name):
            layout.prop(node, self.prop_name, text=text)
        else:
            layout.label(text=f"No '{self.prop_name}' en nodo")

    def draw_color(self, context, node):
        return (0.1, 0.6, 0.8, 1.0)

class RHEM_SocketTurquesaObject(bpy.types.NodeSocket):
    bl_idname = "RHEM_SocketTurquesaObject"
    bl_label = "Socket Turquesa Object"

    prop_name: bpy.props.StringProperty(default="object")

    def draw(self, context, layout, node, text):
        layout.label(text=text if text else self.name)
        
    def draw_color(self, context, node):
        return (0.25, 0.88, 0.82, 1.0)  # RGBA 


class RHEM_SocketMorado(bpy.types.NodeSocket):
    bl_idname = "RHEM_SocketMorado"
    bl_label = "Socket Morado"

    def draw(self, context, layout, node, text):
        layout.label(text=text)

    def draw_color(self, context, node):
        return (0.6, 0.3, 0.8, 1.0)

class RHEM_SocketNaranjaInt(bpy.types.NodeSocket):
    bl_idname = "RHEM_SocketNaranjaInt"
    bl_label = "Socket Naranja Int"

    prop_name: bpy.props.StringProperty(default="valor_x")

    def draw(self, context, layout, node, text):
        if hasattr(node, self.prop_name):
            layout.prop(node, self.prop_name, text=text)
        else:
            layout.label(text=f"'{self.prop_name}' no existe")

    def draw_color(self, context, node):
        return (0.8, 0.4, 0.1, 1.0)
