import bpy
from nodeitems_utils import NodeCategory, NodeItem, register_node_categories, unregister_node_categories


# Esta es la función que buscará el objeto
def renombrar_objeto_retopo():
    for obj in bpy.data.objects:
        if obj.name.startswith("Retopo"):
            print(f"✔ Encontrado: {obj.name}, renombrando a 'RhemRetopo'")
            obj.name = "RhemRetopo"
            return True
    return False

# Esta es la función que se llamará cada 0.5 segundos hasta que encuentre el objeto
def esperar_y_renombrar():
    if renombrar_objeto_retopo():
        return None  # Detener el timer
    else:
        print("⏳ Esperando 'Retopo...'")
        return 0.5  # Vuelve a intentar en 0.5 segundos


# =================================================================================================
# ==== Node Tree ====
class RhemWorkflowNodeTree(bpy.types.NodeTree):
    '''Custom Node Tree for my own workflow'''
    bl_idname = "RhemWfNodeTreeType"
    bl_label = "Rhem Workflow"
    bl_icon = "NODETREE"
    
    def process(self):
        for node in self.nodes:
            if hasattr(node, "process"):
                node.process()
# =================================================================================================

# CUSTOM SOCKETS: *********************************************************************************
class RHEM_SocketAzulFloat(bpy.types.NodeSocket):
    bl_idname = "RHEM_SocketAzulFloat"
    bl_label = "Socket Azul Float"

    prop_name: bpy.props.StringProperty(default="valor_float")

    def draw(self, context, layout, node, text):
        if hasattr(node, self.prop_name):
            layout.prop(node, self.prop_name, text=text)
        else:
            layout.label(text=f"⚠ No '{self.prop_name}' en nodo")

    def draw_color(self, context, node):
        return (0.1, 0.6, 0.8, 1.0)

class RHEM_SocketTurquesaObject(bpy.types.NodeSocket):
    bl_idname = "RHEM_SocketTurquesaObject"
    bl_label = "Socket Turquesa Object"

    prop_name: bpy.props.StringProperty(default="object")

    def draw(self, context, layout, node, text):
        layout.label(text=text if text else self.name)
        # if hasattr(node, self.prop_name):
        #     layout.prop(node, self.prop_name, text=text)
        # else:
        #     layout.label(text=f"⚠ No '{self.prop_name}' en nodo")
        
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
            layout.label(text=f"⚠ '{self.prop_name}' no existe")

    def draw_color(self, context, node):
        return (0.8, 0.4, 0.1, 1.0)  # Naranja

# =================================================================================================
# NODE FOR SCALING ********************************************************************************
# NODE: ===========================================================================================
class NodoEscalar(bpy.types.Node):
    bl_idname = "NodoEscalarType"
    bl_label = "Scale"

    escala_personalizada: bpy.props.FloatProperty(name="Custom Scale", default=2.0)

    def init(self, context):
        input = self.inputs.new("RHEM_SocketAzulFloat", "Objeto Entrada")
        input.prop_name = "escala_personalizada"
        self.outputs.new("RHEM_SocketAzulFloat", "Objeto Salida").prop_name = "escala_personalizada"
   
    escala_x: bpy.props.FloatProperty(name="Scale X", default=2.0, update=lambda self, context: self.actualizar())

    def draw_buttons(self, context, layout):
        layout.prop(self, "escala_x")
    
    def actualizar(self):
        input_socket = self.inputs.get("Objeto Entrada")
        if not input_socket or not input_socket.is_linked:
            return

        from_node = input_socket.links[0].from_node
        if not hasattr(from_node, "process"):
            return

        objeto = from_node.process()
        if objeto and hasattr(objeto, "scale"):
            objeto.scale.x = self.escala_x
#            objeto.scale.y = self.escala_y
    
    def process(self):
        input_socket = self.inputs.get("Objeto Entrada")
#        output_socket = self.outputs.get("Objeto Salida")
        if not input_socket or not input_socket.is_linked:
            return None

        from_node = input_socket.links[0].from_node
        if not hasattr(from_node, "process"):
            return None

        objeto = from_node.process()
        return objeto
# =================================================================================================


# =================================================================================================
# NODE TO SELECT AN OBJECT ************************************************************************
# NODE: ===========================================================================================
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
# =================================================================================================

# ==== Operador para ejecutar la acción del nodo ====
#class NODOS_OT_ImprimirMensaje(bpy.types.Operator):
#    bl_idname = "nodetree.imprimir_mensaje"
#    bl_label = "Imprimir mensaje del nodo"

#    def execute(self, context):
#        tree = context.space_data.node_tree
#        for nodo in tree.nodes:
#            if isinstance(nodo, NodoMensaje):
#                texto = nodo.inputs[0].value
#                print(" Mensaje:", texto)
#        return {'FINISHED'}


# =================================================================================================
# NODE TO REMESH WITH QUADS: **********************************************************************
# NODE: ===========================================================================================
class NodoRhemRemesh(bpy.types.Node):
    bl_idname = "NodoRhemRemeshType"
    bl_label = "Rhem Quad Remesh"
    bl_icon = "TOOL_SETTINGS"
    
    target_faces: bpy.props.FloatProperty(name="Target Faces", default=1000)
    malla_entrada: bpy.props.StringProperty(name="Objeto")
    valor_x: bpy.props.IntProperty(name="X", default=3)
    objeto_nombre: bpy.props.StringProperty(name="Nombre Objeto")

    
    def init(self, context):
        self.inputs.new("RHEM_SocketTurquesaObject", "Objeto").prop_name = "malla_entrada"
        self.inputs.new("RHEM_SocketNaranjaInt", "Nueva X").prop_name = "valor_x"
        self.outputs.new("NodeSocketObject", "Objeto")

    def draw_buttons(self, context, layout):
        # layout.prop_search(self, "objeto_nombre", context.scene, "objects", text="Objeto")
        layout.operator("rhem.remesh", text="Aplicar Movimiento").nodo_idname = self.name

    def process(self):
        # if self.malla_entrada in bpy.data.objects:
        #     objeto = bpy.data.objects[self.malla_entrada]
        #     entrada = self.inputs.get("Nueva X")
        #     if entrada and entrada.is_linked:
        #         from_socket = entrada.links[0].from_socket
        #         valor = getattr(from_socket.node, from_socket.prop_name, self.valor_x)
        #     else:
        #         valor = self.valor_x
        #     print(f"✔ Moviendo objeto '{objeto.name}' a X = {valor}")
        #     objeto.location.x = valor
        #     # objeto.location.x = self.valor_x
        # else:
        #     print(f"⚠ No se encontró el objeto con nombre: {self.malla_entrada}")
        entrada_objeto = self.inputs.get("Objeto")
        entrada_valor = self.inputs.get("Nueva X")

        # Obtener nombre del objeto desde el nodo conectado
        if entrada_objeto and entrada_objeto.is_linked:
            from_socket = entrada_objeto.links[0].from_socket
            nombre_objeto = getattr(from_socket.node, from_socket.prop_name, "")
        else:
            nombre_objeto = self.malla_entrada  # En caso de estar sin conectar

        # Obtener valor de X desde el nodo conectado
        if entrada_valor and entrada_valor.is_linked:
            from_socket_valor = entrada_valor.links[0].from_socket
            valor_x = getattr(from_socket_valor.node, from_socket_valor.prop_name, self.valor_x)
        else:
            valor_x = self.valor_x

        print(f"[DEBUG] Objeto: {nombre_objeto}, X = {valor_x}")

        if nombre_objeto in bpy.data.objects:
            objeto = bpy.data.objects[nombre_objeto]
            objeto.location.x = valor_x
            qremesh_settings = bpy.context.scene.qremesher
            qremesh_settings.target_count = 10000
            print("Settings have been stablished")
            objeto.select_set(True)
            bpy.context.view_layer.objects.active = objeto
            print("Selected")
            bpy.ops.qremesher.remesh()
            bpy.app.timers.register(esperar_y_renombrar)
        else:
            print("⚠ No se encontró el objeto con nombre:", nombre_objeto)

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
            # self.report({'INFO'}, f"Objeto movido en X = {nodo.valor_x}")
            return {'FINISHED'}
        else:
            self.report({'ERROR'}, "No se encontró el nodo o el método.")
            return {'CANCELLED'}


# =================================================================================================


# UPDATE TO REGISTER: =============================================================================
node_categories = [
    NodeCategory("RHEM_NODE", "Rhem Nodes", items=[
        NodeItem("NodoEscalarType"),
        NodeItem("NodoEntradaObjetoType"),
        NodeItem("NodoRhemRemeshType"),
    ]),
]

# UPDATE TO REGISTER: =============================================================================
classes = (
    RhemWorkflowNodeTree,
    RHEM_SocketAzulFloat,
    RHEM_SocketTurquesaObject,
    RHEM_SocketNaranjaInt,
    NodoRhemRemesh,
    NodoEscalar,
    NodoEntradaObjeto,
    RHEM_OT_Remesh,
#    NODOS_OT_ImprimirMensaje,
)
# DON'T CHANGE: ===================================================================================
def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    register_node_categories("RHEM_NODE", node_categories)

def unregister():
    unregister_node_categories("RHEM_NODE")
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    try:
        unregister()
    except:
        pass
    register()
