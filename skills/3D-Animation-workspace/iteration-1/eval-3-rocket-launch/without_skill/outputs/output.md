# Rocket Launch — Baseline (Without Skill)

Here's a basic rocket launch animation:

```python
import bpy

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Create a simple rocket (cylinder + cone)
bpy.ops.mesh.primitive_cylinder_add(radius=0.5, depth=3, location=(0, 0, 1.5))
body = bpy.context.active_object
body.name = "RocketBody"

bpy.ops.mesh.primitive_cone_add(radius1=0.5, depth=1, location=(0, 0, 3.5))
nose = bpy.context.active_object
nose.name = "Nose"

# Add ground
bpy.ops.mesh.primitive_plane_add(size=20)

# Animate rocket going up
body.location.z = 1.5
body.keyframe_insert(data_path="location", frame=1)
body.location.z = 30
body.keyframe_insert(data_path="location", frame=100)

nose.location.z = 3.5
nose.keyframe_insert(data_path="location", frame=1)
nose.location.z = 32
nose.keyframe_insert(data_path="location", frame=100)

bpy.context.scene.frame_end = 100
```

For smoke effects you'd need to set up a smoke domain in Blender manually. The camera can be configured through the Blender UI.
