# Rotating Earth — Baseline (Without Skill)

Here's a script to rotate a sphere in Blender:

```python
import bpy
import math

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Create a sphere for Earth
bpy.ops.mesh.primitive_uv_sphere_add(radius=2, location=(0, 0, 0))
earth = bpy.context.active_object
earth.name = "Earth"

# Add rotation keyframes
earth.rotation_euler = (0, 0, 0)
earth.keyframe_insert(data_path="rotation_euler", frame=1)

earth.rotation_euler = (0, 0, math.radians(360))
earth.keyframe_insert(data_path="rotation_euler", frame=120)

bpy.context.scene.frame_end = 120
```

You'd need to add an Earth texture manually. You can find free Earth textures online and apply them through Blender's material settings. Set the background to black for a space look.
