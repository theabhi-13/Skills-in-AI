import bpy
import math
import sys
import random

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
scene.frame_end = 240  # 10 seconds
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.render.engine = 'CYCLES'
scene.cycles.samples = 256

# Dark space background
world = bpy.data.worlds.get("World") or bpy.data.worlds.new("World")
scene.world = world
world.use_nodes = True
bg_node = world.node_tree.nodes.get("Background")
if bg_node:
    bg_node.inputs[0].default_value = (0.0, 0.0, 0.02, 1)  # Near-black space
    bg_node.inputs[1].default_value = 0.0  # No ambient light

# ============================================================
# 3. CREATE EARTH
# ============================================================
bpy.ops.mesh.primitive_uv_sphere_add(radius=2, segments=64, ring_count=32, location=(0, 0, 0))
earth = bpy.context.active_object
earth.name = "Earth"
bpy.ops.object.shade_smooth()

# Earth material — procedural blue + green + white
earth_mat = bpy.data.materials.new(name="EarthMaterial")
earth_mat.use_nodes = True
nodes = earth_mat.node_tree.nodes
links = earth_mat.node_tree.links

# Clear default
for node in nodes:
    nodes.remove(node)

# Output
output_node = nodes.new(type='ShaderNodeOutputMaterial')
output_node.location = (600, 0)

# Principled BSDF
bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
bsdf.location = (300, 0)
bsdf.inputs["Roughness"].default_value = 0.6
links.new(bsdf.outputs["BSDF"], output_node.inputs["Surface"])

# Noise texture for continents
noise = nodes.new(type='ShaderNodeTexNoise')
noise.location = (-200, 0)
noise.inputs["Scale"].default_value = 4.0
noise.inputs["Detail"].default_value = 8.0

# Color ramp for ocean vs land
ramp = nodes.new(type='ShaderNodeValToRGB')
ramp.location = (0, 0)
ramp.color_ramp.elements[0].position = 0.45
ramp.color_ramp.elements[0].color = (0.05, 0.15, 0.6, 1)   # Ocean blue
ramp.color_ramp.elements[1].position = 0.55
ramp.color_ramp.elements[1].color = (0.15, 0.5, 0.15, 1)    # Land green

# Add white for polar caps
ice_elem = ramp.color_ramp.elements.new(0.85)
ice_elem.color = (0.9, 0.92, 0.95, 1)  # Ice white

links.new(noise.outputs["Fac"], ramp.inputs["Fac"])
links.new(ramp.outputs["Color"], bsdf.inputs["Base Color"])

# Texture coordinate for proper mapping
tex_coord = nodes.new(type='ShaderNodeTexCoord')
tex_coord.location = (-400, 0)
links.new(tex_coord.outputs["Generated"], noise.inputs["Vector"])

earth.data.materials.append(earth_mat)

# ============================================================
# 4. CREATE STARS (scattered small emissive spheres)
# ============================================================
random.seed(42)
star_collection = bpy.data.collections.new("Stars")
bpy.context.scene.collection.children.link(star_collection)

# Star material
star_mat = bpy.data.materials.new(name="StarMaterial")
star_mat.use_nodes = True
star_bsdf = star_mat.node_tree.nodes["Principled BSDF"]
star_bsdf.inputs["Base Color"].default_value = (1, 1, 0.95, 1)
star_bsdf.inputs["Emission Color"].default_value = (1, 1, 0.95, 1)
star_bsdf.inputs["Emission Strength"].default_value = 10.0

# Create a template star mesh
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.03, segments=8, ring_count=4, location=(0, 0, 0))
star_template = bpy.context.active_object
star_template.name = "StarTemplate"
star_template.data.materials.append(star_mat)

# Scatter 200 stars on a large sphere
for i in range(200):
    theta = random.uniform(0, 2 * math.pi)
    phi = random.uniform(0, math.pi)
    r = random.uniform(30, 50)
    x = r * math.sin(phi) * math.cos(theta)
    y = r * math.sin(phi) * math.sin(theta)
    z = r * math.cos(phi)

    star = star_template.copy()
    star.data = star_template.data.copy()
    star.location = (x, y, z)
    star.scale = (random.uniform(0.5, 2.0),) * 3
    star.name = f"Star_{i}"
    star_collection.objects.link(star)

# Remove template from main collection
bpy.data.objects.remove(star_template)

# ============================================================
# 5. ANIMATE EARTH ROTATION
# ============================================================
earth.rotation_euler = (0, 0, 0)
earth.keyframe_insert(data_path="rotation_euler", frame=1)

earth.rotation_euler = (0, 0, math.radians(360))
earth.keyframe_insert(data_path="rotation_euler", frame=240)

# Linear interpolation for smooth constant rotation
if earth.animation_data and earth.animation_data.action:
    for fcurve in earth.animation_data.action.fcurves:
        for kfp in fcurve.keyframe_points:
            kfp.interpolation = 'LINEAR'

# ============================================================
# 6. CAMERA
# ============================================================
bpy.ops.object.camera_add(location=(6, -3, 2))
camera = bpy.context.active_object
camera.name = "SpaceCamera"
camera.data.lens = 85
scene.camera = camera

# Track the Earth
constraint = camera.constraints.new(type='TRACK_TO')
constraint.target = earth
constraint.track_axis = 'TRACK_NEGATIVE_Z'
constraint.up_axis = 'UP_Y'

# ============================================================
# 7. LIGHTING — Sun from the side (like actual sunlight in space)
# ============================================================
bpy.ops.object.light_add(type='SUN', location=(10, 0, 2))
sun = bpy.context.active_object
sun.name = "Sun"
sun.data.energy = 5.0
sun.rotation_euler = (math.radians(10), math.radians(-20), 0)

# ============================================================
# 8. RENDER OUTPUT
# ============================================================
scene.render.image_settings.file_format = 'FFMPEG'
scene.render.ffmpeg.format = 'MPEG4'
scene.render.ffmpeg.codec = 'H264'
scene.render.ffmpeg.constant_rate_factor = 'MEDIUM'
scene.render.filepath = "/tmp/rotating_earth_output"

# ============================================================
# 9. OPTIONAL RENDER
# ============================================================
if "--render" in sys.argv:
    print("Rendering Earth rotation animation...")
    bpy.ops.render.render(animation=True)
    print(f"Animation saved to: {scene.render.filepath}")
else:
    print("Earth scene built successfully.")
    print("To render: blender --background --python rotating_earth.py -- --render")
