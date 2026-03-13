import bpy
import math
import sys

# ============================================================
# 1. CLEAR THE DEFAULT SCENE
# ============================================================
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Remove default collections' leftover data
for col in bpy.data.collections:
    bpy.data.collections.remove(col)

# ============================================================
# 2. SCENE SETTINGS
# ============================================================
scene = bpy.context.scene
scene.render.fps = 24
scene.frame_start = 1
scene.frame_end = 85  # ~3.5 seconds
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.render.engine = 'CYCLES'
scene.cycles.samples = 128

# Background
world = bpy.data.worlds.get("World") or bpy.data.worlds.new("World")
scene.world = world
world.use_nodes = True
bg_node = world.node_tree.nodes.get("Background")
if bg_node:
    bg_node.inputs[0].default_value = (0.82, 0.82, 0.82, 1)  # Light gray

# ============================================================
# 3. CREATE OBJECTS
# ============================================================

# --- Floor (concrete-like) ---
bpy.ops.mesh.primitive_plane_add(size=30, location=(0, 0, 0))
floor = bpy.context.active_object
floor.name = "Floor"

# --- Ball (red rubber) ---
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.5, segments=32, ring_count=16, location=(0, 0, 5))
ball = bpy.context.active_object
ball.name = "Ball"
bpy.ops.object.shade_smooth()

# ============================================================
# 4. MATERIALS
# ============================================================

def create_material(name, color, roughness=0.5, subsurface=0.0):
    """Create a Principled BSDF material."""
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    bsdf.inputs["Roughness"].default_value = roughness
    if subsurface > 0:
        bsdf.inputs["Subsurface Weight"].default_value = subsurface
    return mat

# Red rubber ball material
ball_mat = create_material("RedRubber", (0.8, 0.13, 0.13), roughness=0.35, subsurface=0.1)
ball.data.materials.append(ball_mat)

# Concrete floor material
floor_mat = create_material("Concrete", (0.6, 0.58, 0.55), roughness=0.9)
floor.data.materials.append(floor_mat)

# ============================================================
# 5. KEYFRAME ANIMATION — Bouncing with Squash & Stretch
# ============================================================

bounce_data = {
    1:   {"loc": (0, 0, 5.0),  "scale": (1.0, 1.0, 1.0)},     # start: falling
    18:  {"loc": (0, 0, 0.5),  "scale": (1.3, 1.3, 0.6)},      # hit floor — squash
    30:  {"loc": (0, 0, 3.5),  "scale": (0.85, 0.85, 1.2)},    # bounce up — stretch
    45:  {"loc": (0, 0, 0.5),  "scale": (1.2, 1.2, 0.7)},      # hit floor — squash
    55:  {"loc": (0, 0, 2.0),  "scale": (0.9, 0.9, 1.1)},      # smaller bounce
    68:  {"loc": (0, 0, 0.5),  "scale": (1.1, 1.1, 0.85)},     # hit floor
    75:  {"loc": (0, 0, 1.0),  "scale": (1.0, 1.0, 1.0)},      # tiny bounce
    85:  {"loc": (0, 0, 0.5),  "scale": (1.0, 1.0, 1.0)},      # settle
}

for frame, data in bounce_data.items():
    ball.location = data["loc"]
    ball.scale = data["scale"]
    ball.keyframe_insert(data_path="location", frame=frame)
    ball.keyframe_insert(data_path="scale", frame=frame)

# Set interpolation to Bezier for smooth motion
if ball.animation_data and ball.animation_data.action:
    for fcurve in ball.animation_data.action.fcurves:
        for kfp in fcurve.keyframe_points:
            kfp.interpolation = 'BEZIER'

# ============================================================
# 6. CAMERA — Static side view
# ============================================================
bpy.ops.object.camera_add(location=(10, 0, 3))
camera = bpy.context.active_object
camera.name = "SideCamera"
camera.data.lens = 50
scene.camera = camera

# Point camera at the ball's resting position
camera.rotation_euler = (math.radians(80), 0, math.radians(90))

# ============================================================
# 7. LIGHTING — Three-point setup
# ============================================================

# Key light (Sun)
bpy.ops.object.light_add(type='SUN', location=(5, -5, 10))
key_light = bpy.context.active_object
key_light.name = "KeyLight"
key_light.data.energy = 3.0
key_light.rotation_euler = (math.radians(45), 0, math.radians(45))

# Fill light (Area)
bpy.ops.object.light_add(type='AREA', location=(-5, -3, 5))
fill_light = bpy.context.active_object
fill_light.name = "FillLight"
fill_light.data.energy = 50
fill_light.data.size = 3

# Rim light (Point)
bpy.ops.object.light_add(type='POINT', location=(0, 5, 6))
rim_light = bpy.context.active_object
rim_light.name = "RimLight"
rim_light.data.energy = 200

# ============================================================
# 8. RENDER OUTPUT
# ============================================================
scene.render.image_settings.file_format = 'FFMPEG'
scene.render.ffmpeg.format = 'MPEG4'
scene.render.ffmpeg.codec = 'H264'
scene.render.ffmpeg.constant_rate_factor = 'MEDIUM'
scene.render.filepath = "/tmp/bouncing_ball_output"

# ============================================================
# 9. OPTIONAL: Render if --render flag is passed
# ============================================================
if "--render" in sys.argv:
    print("Rendering animation...")
    bpy.ops.render.render(animation=True)
    print(f"Animation saved to: {scene.render.filepath}")
else:
    print("Scene built successfully.")
    print("To render, run: blender --background --python bouncing_ball.py -- --render")
