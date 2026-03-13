import bpy
import os

# Create the output directory
output_dir = "/Users/theabhi_13/Desktop/Skills_Tutorial/skills/3D-Animation-workspace/verification/outputs/"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Clear the scene
bpy.ops.wm.read_factory_settings(use_empty=True)

# Add a floor
bpy.ops.mesh.primitive_plane_add(size=10, location=(0, 0, 0))
floor = bpy.context.active_object
floor.name = "Floor"

# Add a ball
bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=(0, 0, 5))
ball = bpy.context.active_object
ball.name = "Ball"

# Add materials
def create_material(name, color, roughness):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    bsdf = nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = color
        bsdf.inputs["Roughness"].default_value = roughness
    return mat

ball_mat = create_material("BallMat", (1, 0, 0, 1), 0.5)
ball.data.materials.append(ball_mat)

floor_mat = create_material("FloorMat", (0.4, 0.4, 0.4, 1), 0.8)
floor.data.materials.append(floor_mat)

# Animation
fps = 24
bpy.context.scene.render.fps = fps
bpy.context.scene.frame_start = 1
bpy.context.scene.frame_end = 120

# Set default interpolation to Bezier
bpy.context.preferences.edit.keyframe_new_interpolation_type = 'BEZIER'

# Keyframes for bouncing
keyframes = [
    (1, 5), (15, 1), (30, 4), (45, 1), (60, 3), (75, 1), (90, 2), (105, 1), (120, 1)
]

for frame, z in keyframes:
    ball.location.z = z
    ball.keyframe_insert(data_path="location", frame=frame, index=2)

# Camera
bpy.ops.object.camera_add(location=(15, 0, 3), rotation=(1.5708, 0, 1.5708))
cam = bpy.context.active_object
bpy.context.scene.camera = cam

# Light
bpy.ops.object.light_add(type='SUN', location=(10, 10, 10))

# Render settings (PNG Sequence)
bpy.context.scene.render.engine = 'BLENDER_EEVEE'
bpy.context.scene.render.image_settings.file_format = 'PNG'
bpy.context.scene.render.filepath = os.path.join(output_dir, "frame_")

# Render animation
bpy.ops.render.render(animation=True)
