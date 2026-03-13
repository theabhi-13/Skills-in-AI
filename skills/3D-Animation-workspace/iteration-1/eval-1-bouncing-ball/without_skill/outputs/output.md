# Bouncing Ball — Baseline (Without Skill)

Here's a basic bouncing ball animation in Blender:

```python
import bpy

# Delete default objects
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Add a sphere
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.5, location=(0, 0, 3))
ball = bpy.context.active_object

# Add a plane for the floor
bpy.ops.mesh.primitive_plane_add(size=10, location=(0, 0, 0))

# Animate the ball bouncing
ball.location = (0, 0, 3)
ball.keyframe_insert(data_path="location", frame=1)

ball.location = (0, 0, 0.5)
ball.keyframe_insert(data_path="location", frame=20)

ball.location = (0, 0, 2)
ball.keyframe_insert(data_path="location", frame=40)

ball.location = (0, 0, 0.5)
ball.keyframe_insert(data_path="location", frame=60)

# Set render settings
bpy.context.scene.frame_end = 60
```

You can run this in Blender's scripting tab or from the command line with `blender --python script.py`.
