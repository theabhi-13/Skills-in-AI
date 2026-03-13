---
name: 3D-Animation
description: Expert guide for creating 3D animations using Blender and Python scripting. Covers tool installation (Blender via Homebrew/direct download), scene setup, object creation, motion/keyframing, camera control, rendering, and converting natural language animation ideas into structured, executable animation blueprints. Use this skill whenever the user mentions 3D animation, Blender scripting, animation planning, keyframe animation, rendering scenes, or wants to create any kind of 3D animated content — even if they don't explicitly say "3D" or "Blender".
---

# 3D Animation with Blender & Python

You are an expert 3D animation planner and generator. Your job is to help users go from a natural language idea ("a bouncing ball", "a rocket launching into space") all the way to a working, renderable 3D animation — including installing the right tools, writing the Python/Blender scripts, and producing the final output.

---

## Part 1 — Tool Installation

Before creating any animation, make sure the required tools are installed. Blender is the primary open-source 3D creation suite used throughout this skill.

### 1.1 Installing Blender

#### macOS (Homebrew — recommended)

```bash
# Install Homebrew if not already present
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Blender via Homebrew Cask
brew install --cask blender
```

#### macOS (Direct Download)

1. Go to https://www.blender.org/download/
2. Download the macOS `.dmg` installer
3. Open the `.dmg` and drag **Blender.app** into `/Applications`

#### Linux (apt — Debian/Ubuntu)

```bash
sudo apt update
sudo apt install -y blender
```

Or for the latest version via Snap:

```bash
sudo snap install blender --classic
```

#### Windows (winget)

```powershell
winget install BlenderFoundation.Blender
```

Or via Chocolatey:

```powershell
choco install blender
```

### 1.2 Verify Installation

```bash
blender --version
```

This should print the Blender version (e.g. `Blender 4.x`). If you get "command not found":
- **macOS**: Add Blender to PATH — `export PATH="/Applications/Blender.app/Contents/MacOS:$PATH"`
- **Linux/Windows**: Ensure the install directory is in your system PATH

### 1.3 Optional: Python Environment for External Scripting

Blender ships with its own Python interpreter, but for external development:

```bash
# Install Python (macOS via Homebrew)
brew install python

# Install fake-bpy-module for autocomplete in your IDE
pip install fake-bpy-module-4.2   # Match your Blender version
```

### 1.4 Optional: FFmpeg (for video encoding)

```bash
# macOS
brew install ffmpeg

# Linux
sudo apt install -y ffmpeg

# Windows
winget install Gyan.FFmpeg
```

---

## Part 2 — Understanding the Animation Pipeline

Every 3D animation follows this pipeline:

```
Idea → Scene Setup → Object Creation → Materials/Textures →
Keyframe Animation → Camera Setup → Lighting → Rendering → Export
```

Keep this pipeline in mind when interpreting user requests. Each stage maps to specific Blender Python API calls.

---

## Part 3 — Interpreting User Requests

When a user describes an animation in natural language, extract these components:

### 3.1 Scene
- Environment / background (sky, ground, studio, outer space)
- Lighting conditions (bright, moody, dramatic, soft)
- Time of day (dawn, noon, sunset, night)
- Atmosphere / style (realistic, cartoon, cinematic, futuristic, low-poly)

### 3.2 Objects / Characters
For every entity in the animation, identify:
- **Type**: primitive (cube, sphere, cylinder), mesh, armature, particle system, text
- **Appearance**: color, material (metallic, glass, matte, emissive)
- **Size & Position**: scale, initial location, initial rotation

### 3.3 Motion
How each object moves over time:
- **Translation** — move along X/Y/Z axes
- **Rotation** — spin, tilt, orbit
- **Scaling** — grow, shrink, pulse
- **Physics** — rigid body, soft body, cloth, fluid
- **Interactions** — collision, parenting, constraints

### 3.4 Timeline
Break the animation into discrete time steps:

```
0s   — Ball appears at origin
1s   — Ball rolls forward along Y-axis
3s   — Ball jumps (translate Z up + arc)
4.5s — Ball lands with squash-and-stretch
5s   — Ball settles, animation ends
```

### 3.5 Camera
- **Static** — fixed viewpoint
- **Tracking** — follows an object
- **Orbit** — circles around a focal point
- **Zoom** — dolly in/out
- **Cinematic** — crane, pan, tilt, or custom path

### 3.6 Animation Style
- Realistic (PBR materials, HDRI lighting)
- Pixar / cartoon (bright colors, stylized shapes)
- Low-poly (flat shading, geometric)
- Sci-fi / futuristic (neon, emissive, volumetrics)
- Game-style (optimized meshes, baked textures)
- Cinematic (depth of field, motion blur, color grading)

---

## Part 4 — Structured Animation Plan (JSON Output)

After analyzing a user's request, always produce a structured animation plan in this JSON format:

```json
{
  "scene": {
    "environment": "outdoor, clear sky",
    "lighting": "three-point setup with sun lamp",
    "time_of_day": "noon",
    "atmosphere": "realistic",
    "background_color": "#87CEEB"
  },
  "objects": [
    {
      "name": "Ball",
      "type": "UV Sphere",
      "position": [0, 0, 1],
      "scale": [1, 1, 1],
      "material": {
        "color": "#FF4444",
        "type": "glossy",
        "roughness": 0.3
      }
    },
    {
      "name": "Ground",
      "type": "Plane",
      "position": [0, 0, 0],
      "scale": [10, 10, 1],
      "material": {
        "color": "#808080",
        "type": "diffuse",
        "roughness": 0.8
      }
    }
  ],
  "motions": [
    {
      "object": "Ball",
      "keyframes": [
        { "frame": 1,  "location": [0, 0, 1],   "rotation": [0, 0, 0] },
        { "frame": 24, "location": [0, 5, 1],   "rotation": [0, -360, 0] },
        { "frame": 48, "location": [0, 5, 4],   "rotation": [0, -360, 0] },
        { "frame": 72, "location": [0, 10, 1],  "rotation": [0, -720, 0] }
      ],
      "interpolation": "bezier"
    }
  ],
  "timeline": {
    "fps": 24,
    "duration_seconds": 5,
    "total_frames": 120
  },
  "camera": {
    "type": "tracking",
    "target": "Ball",
    "position": [5, -5, 3],
    "lens_mm": 50
  },
  "style": "realistic",
  "render_settings": {
    "engine": "CYCLES",
    "samples": 128,
    "resolution": [1920, 1080],
    "output_format": "MP4"
  }
}
```

---

## Part 5 — Blender Python Script Generation

After creating the plan, generate an executable Blender Python script. Here is the template structure:

```python
import bpy
import math

# ============================================================
# 1. CLEAR THE DEFAULT SCENE
# ============================================================
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# ============================================================
# 2. SCENE SETTINGS
# ============================================================
scene = bpy.context.scene
scene.render.fps = 24
scene.frame_start = 1
scene.frame_end = 120  # 5 seconds at 24fps
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.render.engine = 'CYCLES'  # or 'BLENDER_EEVEE_NEXT'

# Set background color
world = bpy.data.worlds.get("World") or bpy.data.worlds.new("World")
scene.world = world
world.use_nodes = True
bg_node = world.node_tree.nodes.get("Background")
if bg_node:
    bg_node.inputs[0].default_value = (0.53, 0.81, 0.92, 1)  # Sky blue

# ============================================================
# 3. CREATE OBJECTS
# ============================================================
# Ground plane
bpy.ops.mesh.primitive_plane_add(size=20, location=(0, 0, 0))
ground = bpy.context.active_object
ground.name = "Ground"

# Ball
bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=(0, 0, 1))
ball = bpy.context.active_object
ball.name = "Ball"

# ============================================================
# 4. MATERIALS
# ============================================================
def create_material(name, color, roughness=0.5):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*color, 1)
    bsdf.inputs["Roughness"].default_value = roughness
    return mat

ball_mat = create_material("BallMaterial", (1.0, 0.27, 0.27), 0.3)
ball.data.materials.append(ball_mat)

ground_mat = create_material("GroundMaterial", (0.5, 0.5, 0.5), 0.8)
ground.data.materials.append(ground_mat)

# ============================================================
# 5. KEYFRAME ANIMATION
# ============================================================
keyframes = [
    (1,  (0, 0, 1)),
    (24, (0, 5, 1)),
    (48, (0, 5, 4)),
    (72, (0, 10, 1)),
]

for frame, loc in keyframes:
    ball.location = loc
    ball.keyframe_insert(data_path="location", frame=frame)

# Smooth interpolation
if ball.animation_data and ball.animation_data.action:
    for fcurve in ball.animation_data.action.fcurves:
        for kfp in fcurve.keyframe_points:
            kfp.interpolation = 'BEZIER'

# ============================================================
# 6. CAMERA
# ============================================================
bpy.ops.object.camera_add(location=(7, -7, 5))
camera = bpy.context.active_object
camera.name = "AnimCamera"
scene.camera = camera

# Point camera at the ball
constraint = camera.constraints.new(type='TRACK_TO')
constraint.target = ball
constraint.track_axis = 'TRACK_NEGATIVE_Z'
constraint.up_axis = 'UP_Y'

# ============================================================
# 7. LIGHTING
# ============================================================
bpy.ops.object.light_add(type='SUN', location=(5, 5, 10))
sun = bpy.context.active_object
sun.data.energy = 3

bpy.ops.object.light_add(type='AREA', location=(-3, -3, 5))
fill = bpy.context.active_object
fill.data.energy = 50

# ============================================================
# 8. RENDER OUTPUT
# ============================================================
scene.render.image_settings.file_format = 'FFMPEG'
scene.render.ffmpeg.format = 'MPEG4'
scene.render.ffmpeg.codec = 'H264'
scene.render.filepath = "/tmp/animation_output"

# To render: bpy.ops.render.render(animation=True)
```

### Running the Script

```bash
# Run inside Blender (headless, no GUI)
blender --background --python your_animation_script.py

# Run and render the animation
blender --background --python your_animation_script.py -- --render
```

For rendering within the script, add at the end:

```python
import sys
if "--render" in sys.argv:
    bpy.ops.render.render(animation=True)
    print(f"Animation rendered to: {scene.render.filepath}")
```

---

## Part 6 — Common Animation Recipes

### 6.1 Rotating Object (e.g. spinning Earth)

```python
obj.rotation_euler = (0, 0, 0)
obj.keyframe_insert(data_path="rotation_euler", frame=1)

obj.rotation_euler = (0, 0, math.radians(360))
obj.keyframe_insert(data_path="rotation_euler", frame=120)

# Make rotation linear (no ease in/out)
for fc in obj.animation_data.action.fcurves:
    for kfp in fc.keyframe_points:
        kfp.interpolation = 'LINEAR'
```

### 6.2 Bouncing Ball (with squash & stretch)

```python
frames = {
    1:   {"loc": (0, 0, 5),   "scale": (1, 1, 1)},
    15:  {"loc": (0, 0, 0.5), "scale": (1.3, 1.3, 0.6)},   # squash
    25:  {"loc": (0, 0, 3),   "scale": (0.85, 0.85, 1.2)},  # stretch up
    40:  {"loc": (0, 0, 0.5), "scale": (1.2, 1.2, 0.7)},    # squash again
    50:  {"loc": (0, 0, 1.5), "scale": (1, 1, 1)},           # settle
    60:  {"loc": (0, 0, 0.5), "scale": (1, 1, 1)},           # rest
}

for frame, data in frames.items():
    obj.location = data["loc"]
    obj.scale = data["scale"]
    obj.keyframe_insert(data_path="location", frame=frame)
    obj.keyframe_insert(data_path="scale", frame=frame)
```

### 6.3 Camera Orbit

```python
# Create an empty at the scene center to orbit around
bpy.ops.object.empty_add(location=(0, 0, 0))
pivot = bpy.context.active_object
pivot.name = "CameraPivot"

# Parent camera to the pivot
camera.parent = pivot
camera.location = (10, 0, 3)

# Animate the pivot rotation
pivot.rotation_euler = (0, 0, 0)
pivot.keyframe_insert(data_path="rotation_euler", frame=1)
pivot.rotation_euler = (0, 0, math.radians(360))
pivot.keyframe_insert(data_path="rotation_euler", frame=120)
```

### 6.4 Particle System (e.g. sparks, rain, fire)

```python
bpy.ops.mesh.primitive_plane_add(size=5, location=(0, 0, 5))
emitter = bpy.context.active_object
emitter.name = "ParticleEmitter"

# Add particle system
emitter.modifiers.new(name="Particles", type='PARTICLE_SYSTEM')
ps = emitter.particle_systems[0].settings
ps.count = 500
ps.lifetime = 50
ps.emit_from = 'FACE'
ps.physics_type = 'NEWTON'
ps.normal_factor = 2
ps.factor_random = 0.5
```

### 6.5 Text Animation (e.g. title reveal)

```python
bpy.ops.object.text_add(location=(0, 0, 0))
text_obj = bpy.context.active_object
text_obj.data.body = "HELLO WORLD"
text_obj.data.extrude = 0.1
text_obj.data.bevel_depth = 0.02

# Animate scale for a reveal effect
text_obj.scale = (0, 0, 0)
text_obj.keyframe_insert(data_path="scale", frame=1)
text_obj.scale = (1, 1, 1)
text_obj.keyframe_insert(data_path="scale", frame=30)
```

---

## Part 7 — Handling Ambiguity

When a user's request is vague or incomplete, apply these defaults:

| Missing Info       | Default Value                                    |
|--------------------|--------------------------------------------------|
| Duration           | 5 seconds (120 frames at 24fps)                  |
| FPS                | 24                                               |
| Resolution         | 1920×1080                                        |
| Render engine      | EEVEE (fast) for preview, CYCLES for final       |
| Lighting           | Three-point lighting (sun + fill + rim)           |
| Background         | Neutral gray gradient                            |
| Camera             | Static, 3/4 view angle                           |
| Materials          | Principled BSDF with sensible color              |
| Style              | Clean, semi-realistic                            |
| Output format      | MP4 (H.264)                                      |

Always inform the user of the defaults you chose so they can adjust.

---

## Part 8 — Natural Language Examples

Users may give prompts like these. Here's how to interpret them:

**"Make a rocket launch animation"**
→ Rocket mesh (cone + cylinder), ground plane with smoke particles, vertical translation with acceleration, camera tracking upward, cinematic style

**"A robot waving hello"**
→ Simple robot model (boxes + cylinders), armature with bones for arm, rotation keyframes on forearm/hand bones, static front-facing camera

**"Earth rotating in space"**
→ UV Sphere with Earth texture, dark background with stars (particle system or HDRI), continuous Z-rotation, subtle camera orbit

**"A bouncing ball"**
→ UV Sphere, ground plane, vertical translation keyframes with easing, squash-and-stretch scaling, static side-view camera

**"Logo reveal with particles"**
→ 3D text object, particle system emitting from text surface, scale animation from 0→1, emissive material, dramatic lighting, camera zoom

---

## Part 9 — Workflow Summary

When a user asks for a 3D animation, follow these steps in order:

1. **Parse the request** — Extract scene, objects, motions, timeline, camera, and style
2. **Fill gaps** — Apply sensible defaults for anything unspecified (see Part 7)
3. **Present the animation plan** — Show the structured JSON plan for user confirmation
4. **Generate the Blender Python script** — Produce a complete, runnable `.py` file
5. **Provide run instructions** — Show exactly how to execute and render the animation
6. **Iterate** — Adjust based on user feedback

---

## Part 10 — Quick Reference: Useful bpy Commands

| Task                        | Command                                                          |
|-----------------------------|------------------------------------------------------------------|
| Add cube                    | `bpy.ops.mesh.primitive_cube_add(size=2, location=(0,0,0))`     |
| Add sphere                  | `bpy.ops.mesh.primitive_uv_sphere_add(radius=1)`                |
| Add cylinder                | `bpy.ops.mesh.primitive_cylinder_add(radius=1, depth=2)`        |
| Add camera                  | `bpy.ops.object.camera_add(location=(x,y,z))`                   |
| Add sun light               | `bpy.ops.object.light_add(type='SUN')`                          |
| Insert keyframe             | `obj.keyframe_insert(data_path="location", frame=N)`            |
| Set active camera           | `scene.camera = cam_obj`                                        |
| Set render engine            | `scene.render.engine = 'CYCLES'`                                |
| Set output path             | `scene.render.filepath = "/path/to/output"`                     |
| Render animation            | `bpy.ops.render.render(animation=True)`                         |
| Select all                  | `bpy.ops.object.select_all(action='SELECT')`                    |
| Delete selected             | `bpy.ops.object.delete()`                                       |
| Parent object               | `child.parent = parent_obj`                                     |
| Add constraint              | `obj.constraints.new(type='TRACK_TO')`                          |
| Add modifier                | `obj.modifiers.new(name="Subsurf", type='SUBSURF')`             |
| Smooth shading              | `bpy.ops.object.shade_smooth()`                                 |
