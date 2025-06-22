import bpy
import sys

BLENDER_NODES_DIR = r"D:\Varios\My Path\3D Design\Blender - Orthosis\develop\NodesBl\nodes"
if BLENDER_NODES_DIR not in sys.path:
    sys.path.insert(0, BLENDER_NODES_DIR)

try:
    from base_node import RHEM_SocketTurquesaObject, RHEM_SocketAzulFloat
except ImportError as e:
    print(f"Error de importación: {e}")
    raise


class NodoDisplace(bpy.types.Node):
    bl_idname = "NodoDisplaceType"
    bl_label = "Displace"
    bl_icon = "MOD_DISPLACE"

    strength: bpy.props.FloatProperty(name="Strength", default=3.0,
                                      update=lambda self, context: self.actualizar_displace())
    objeto_entrada: bpy.props.StringProperty(name="Input Object")

    def init(self, context):
        self.inputs.new("RHEM_SocketTurquesaObject", "Input Object").prop_name = "objeto_entrada"
        self.inputs.new("RHEM_SocketAzulFloat", "Strength").prop_name = "strength"
        self.outputs.new("RHEM_SocketTurquesaObject", "Output Object")

    def actualizar_displace(self):
        """Actualiza el modificador existente sin crear uno nuevo"""
        new_obj = self.obtener_objeto_salida()
        if not new_obj:
            return
        displace_mod = self.obtener_displace_mod(new_obj)
        if displace_mod:
            displace_mod.strength = self.obtener_strength_actual()

    def obtener_strength_actual(self):
        """Obtiene el valor de strength desde el socket o la propiedad"""
        strength_socket = self.inputs.get("Strength")
        if strength_socket and strength_socket.is_linked:
            from_strength_socket = strength_socket.links[0].from_socket
            return getattr(from_strength_socket.node, from_strength_socket.prop_name, self.strength)
        return self.strength

    def obtener_objeto_salida(self):
        """Obtiene o crea el objeto de salida"""
        input_obj_socket = self.inputs.get("Input Object")
        if not input_obj_socket or not input_obj_socket.is_linked:
            return None
            
        from_socket = input_obj_socket.links[0].from_socket
        obj_name = getattr(from_socket.node, from_socket.prop_name, "")
        
        if not obj_name or obj_name not in bpy.data.objects:
            return None
            
        original_obj = bpy.data.objects[obj_name]
        new_obj_name = f"02 Displaced"
        
        if new_obj_name in bpy.data.objects:
            return bpy.data.objects[new_obj_name]
        else:
            new_obj = original_obj.copy()
            new_obj.data = original_obj.data.copy()
            new_obj.name = new_obj_name
            bpy.context.collection.objects.link(new_obj)
            return new_obj

    def obtener_displace_mod(self, obj):
        """Obtiene o crea el modificador displace"""
        # Buscar modificador existente
        for mod in obj.modifiers:
            if mod.type == 'DISPLACE':
                return mod
        # Crear nuevo si no existe
        new_mod = obj.modifiers.new(name="Displace", type='DISPLACE')
        return new_mod

    def process(self):
        """Método principal llamado por el node tree"""
        new_obj = self.obtener_objeto_salida()
        if not new_obj:
            return None
            
        displace_mod = self.obtener_displace_mod(new_obj)
        if displace_mod:
            displace_mod.strength = self.obtener_strength_actual()
        
        return new_obj