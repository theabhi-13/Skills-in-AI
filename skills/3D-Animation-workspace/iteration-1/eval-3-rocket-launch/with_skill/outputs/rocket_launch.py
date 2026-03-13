import bpy
import math
import sys

# ============================================================
# 1. CLEAR SCENE
# ============================================================
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# ============================================================
# 2. SCENE SETTINGS
# ============================================================
scene = bpy.context.scene
scene.render.fps = 24
scene.frame_start = 1
scene.frame_end = 200  # ~8 seconds
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.render.engine = 'CYCLES'
scene.cycles.samples = 256

# Dark dusk sky background
world = bpy.data.worlds.get("World") or bpy.data.worlds.new("World")
scene.world = world
world.use_nodes = True
bg_node = world.node_tree.nodes.get("Background")
if bg_node:
    bg_node.inputs[0].default_value = (0.1, 0.1, 0.18, 1)  # Dark blue dusk

# ============================================================
# 3. CREATE ROCKET (cone nose + cylinder body + fins)
# ============================================================

# Rocket body (cylinder)
bpy.ops.mesh.primitive_cylinder_add(radius=0.4, depth=4, location=(0, 0, 2))
body = bpy.context.active_object
body.name = "RocketBody"

# Rocket nose cone
bpy.ops.mesh.primitive_cone_add(radius1=0.4, radius2=0, depth=1.2, location=(0, 0, 4.6))
nose = bpy.context.active_object
nose.name = "RocketNose"

# Rocket engine nozzle
bpy.ops.mesh.primitive_cone_add(radius1=0.35, radius2=0.2, depth=0.5, location=(0, 0, -0.25))
nozzle = bpy.context.active_object
nozzle.name = "RocketNozzle"
nozzle.rotation_euler = (math.radians(180), 0, 0)

# Fins (4 flat cubes)
fins = []
for i in range(4):
    angle = math.radians(90 * i)
    x = 0.5 * math.cos(angle)
    y = 0.5 * math.sin(angle)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, 0.5))
    fin = bpy.context.active_object
    fin.name = f"Fin_{i}"
    fin.scale = (0.05, 0.4, 0.6)
    fin.rotation_euler = (0, 0, angle)
    fins.append(fin)

# Create a parent empty for the rocket
bpy.ops.object.empty_add(location=(0, 0, 0))
rocket_parent = bpy.context.active_object
rocket_parent.name = "Rocket"

# Parent all parts to the Rocket empty
for obj in [body, nose, nozzle] + fins:
    obj.parent = rocket_parent

# ============================================================
# 4. MATERIALS
# ============================================================

def create_material(name, color, metallic=0.0, roughness=0.5):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*color, 1)
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["Roughness"].default_value = roughness
    return mat

# Rocket body — white metallic
rocket_mat = create_material("RocketMetal", (0.9, 0.9, 0.92), metallic=0.8, roughness=0.2)
for obj in [body, nose, nozzle]:
    obj.data.materials.append(rocket_mat)

# Fins — dark gray
fin_mat = create_material("FinMaterial", (0.2, 0.2, 0.22), metallic=0.6, roughness=0.3)
for fin in fins:
    fin.data.materials.append(fin_mat)

# Nozzle — dark with emission
nozzle_glow = bpy.data.materials.new(name="NozzleGlow")
nozzle_glow.use_nodes = True
nz_bsdf = nozzle_glow.node_tree.nodes["Principled BSDF"]
nz_bsdf.inputs["Base Color"].default_value = (0.1, 0.1, 0.1, 1)
nz_bsdf.inputs["Emission Color"].default_value = (1.0, 0.4, 0.05, 1)
nz_bsdf.inputs["Emission Strength"].default_value = 5.0
nozzle.data.materials.clear()
nozzle.data.materials.append(nozzle_glow)

# ============================================================
# 5. GROUND PLANE
# ============================================================
bpy.ops.mesh.primitive_plane_add(size=60, location=(0, 0, 0))
ground = bpy.context.active_object
ground.name = "Ground"
ground_mat = create_material("LaunchPad", (0.23, 0.23, 0.23), roughness=0.95)
ground.data.materials.append(ground_mat)

# ============================================================
# 6. PARTICLE SYSTEM — Smoke & Fire
# ============================================================
bpy.ops.mesh.primitive_plane_add(size=1.5, location=(0, 0, 0.1))
emitter = bpy.context.active_object
emitter.name = "SmokeFireEmitter"

# Add particle system
emitter.modifiers.new(name="SmokeParticles", type='PARTICLE_SYSTEM')
ps = emitter.particle_systems[0].settings
ps.name = "SmokeSettings"
ps.count = 2000
ps.lifetime = 40
ps.frame_start = 1
ps.frame_end = 200
ps.emit_from = 'FACE'
ps.physics_type = 'NEWTON'
ps.normal_factor = 3
ps.factor_random = 1.5
ps.use_dynamic_rotation = True

# Smoke particle material (orange-to-gray gradient feel)
smoke_mat = bpy.data.materials.new(name="SmokeMaterial")
smoke_mat.use_nodes = True
s_bsdf = smoke_mat.node_tree.nodes["Principled BSDF"]
s_bsdf.inputs["Base Color"].default_value = (0.8, 0.4, 0.1, 1)
s_bsdf.inputs["Roughness"].default_value = 1.0

# Parent emitter to rocket so smoke follows
emitter.parent = rocket_parent

# ============================================================
# 7. KEYFRAME ANIMATION — Rocket launch with acceleration
# ============================================================
launch_keyframes = {
    1:   (0, 0, 0),      # idle on pad
    30:  (0, 0, 0),      # engines firing, still on pad
    60:  (0, 0, 2),      # slow lift-off
    90:  (0, 0, 8),      # accelerating
    120: (0, 0, 20),     # faster
    160: (0, 0, 50),     # fast
    200: (0, 0, 120),    # gone
}

for frame, loc in launch_keyframes.items():
    rocket_parent.location = loc
    rocket_parent.keyframe_insert(data_path="location", frame=frame)

# Ease-in interpolation for realistic acceleration
if rocket_parent.animation_data and rocket_parent.animation_data.action:
    for fcurve in rocket_parent.animation_data.action.fcurves:
        for kfp in fcurve.keyframe_points:
            kfp.interpolation = 'BEZIER'
            kfp.handle_left_type = 'AUTO'
            kfp.handle_right_type = 'AUTO'

# ============================================================
# 8. CAMERA — Cinematic, tracks the rocket
# ============================================================
bpy.ops.object.camera_add(location=(15, -10, 3))
camera = bpy.context.active_object
camera.name = "CinemaCamera"
camera.data.lens = 35
scene.camera = camera

# Track To constraint — camera follows the rocket
track = camera.constraints.new(type='TRACK_TO')
track.target = rocket_parent
track.track_axis = 'TRACK_NEGATIVE_Z'
track.up_axis = 'UP_Y'

# ============================================================
# 9. LIGHTING — Dramatic cinematic setup
# ============================================================

# Warm key light (sunset feel)
bpy.ops.object.light_add(type='SUN', location=(10, -5, 15))
key = bpy.context.active_object
key.name = "KeyLight"
key.data.energy = 4.0
key.data.color = (1.0, 0.85, 0.7)  # Warm
key.rotation_euler = (math.radians(40), 0, math.radians(30))

# Blue rim light
bpy.ops.object.light_add(type='AREA', location=(-8, 5, 10))
rim = bpy.context.active_object
rim.name = "RimLight"
rim.data.energy = 100
rim.data.color = (0.5, 0.6, 1.0)  # Cool blue
rim.data.size = 5

# Ground fill
bpy.ops.object.light_add(type='POINT', location=(0, 0, 1))
glow = bpy.context.active_object
glow.name = "EngineGlow"
glow.data.energy = 500
glow.data.color = (1.0, 0.5, 0.1)  # Orange fire glow
glow.parent = rocket_parent  # Moves with rocket

# ============================================================
# 10. RENDER OUTPUT
# ============================================================
scene.render.image_settings.file_format = 'FFMPEG'
scene.render.ffmpeg.format = 'MPEG4'
scene.render.ffmpeg.codec = 'H264'
scene.render.ffmpeg.constant_rate_factor = 'MEDIUM'
scene.render.filepath = "/tmp/rocket_launch_output"

# ============================================================
# 11. OPTIONAL RENDER
# ============================================================
if "--render" in sys.argv:
    print("Rendering rocket launch animation...")
    bpy.ops.render.render(animation=True)
    print(f"Animation saved to: {scene.render.filepath}")
else:
    print("Rocket launch scene built successfully.")
    print("To render: blender --background --python rocket_launch.py -- --render")
