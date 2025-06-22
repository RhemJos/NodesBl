import bpy

# Esta es la función que buscará el objeto
def renombrar_objeto_retopo(new_name):
    for obj in bpy.data.objects:
        if obj.name.startswith("Retopo"):
            print(f"Found: {obj.name}, renaming to {new_name}")
            obj.name = new_name
            return True
    return False

# Esta es la función que se llamará cada 0.5 segundos hasta que encuentre el objeto
def esperar_y_renombrar(new_name):
    if renombrar_objeto_retopo(new_name):
        return None  # Detener el timer
    else:
        print("Waiting...")
        return 0.5  # Vuelve a intentar en 0.5 segundos

class NodoRhemRemesh(bpy.types.Node):
    bl_idname = "NodoRhemRemeshType"
    bl_label = "Rhem Quad Remesh"
    bl_icon = "TOOL_SETTINGS"
    
    target_faces: bpy.props.IntProperty(name="Target Faces", default=1000)
    malla_entrada: bpy.props.StringProperty(name="Objeto")
    valor_x: bpy.props.IntProperty(name="X", default=3)
    objeto_nombre: bpy.props.StringProperty(name="Nombre Objeto")

    
    def init(self, context):
        self.inputs.new("RHEM_SocketTurquesaObject", "Objeto").prop_name = "malla_entrada"
        self.inputs.new("RHEM_SocketNaranjaInt", "Target Faces").prop_name = "target_faces"
        self.outputs.new("NodeSocketObject", "Objeto")

    def draw_buttons(self, context, layout):
        # layout.prop_search(self, "objeto_nombre", context.scene, "objects", text="Objeto")
        layout.operator("rhem.remesh", text="Rhemmesh").nodo_idname = self.name

    def process(self):
        entrada_objeto = self.inputs.get("Objeto")
        target_faces = self.inputs.get("Target Faces")

        # Obtener nombre del objeto desde el nodo conectado
        if entrada_objeto and entrada_objeto.is_linked:
            from_socket = entrada_objeto.links[0].from_socket
            nombre_objeto = getattr(from_socket.node, from_socket.prop_name, "")
        else:
            nombre_objeto = self.malla_entrada  # En caso de estar sin conectar

        # Obtener valor de X desde el nodo conectado
        if target_faces and target_faces.is_linked:
            from_socket_valor = target_faces.links[0].from_socket
            target_faces_value = getattr(from_socket_valor.node, from_socket_valor.prop_name, self.target_faces)
        else:
            target_faces_value = self.target_faces

        if nombre_objeto in bpy.data.objects:
            objeto = bpy.data.objects[nombre_objeto]
            qremesh_settings = bpy.context.scene.qremesher
            qremesh_settings.target_count = target_faces_value
            print("Settings have been stablished")
            objeto.select_set(True)
            bpy.context.view_layer.objects.active = objeto
            print("Selected")
            print("Cuac")
            bpy.ops.qremesher.remesh()
            bpy.app.timers.register(lambda: esperar_y_renombrar("Renombre"))
        else:
            print("The object couldn't be found:", nombre_objeto)