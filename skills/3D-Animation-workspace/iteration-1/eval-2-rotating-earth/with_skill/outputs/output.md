# Rotating Earth in Space — With Skill Output

## Animation Plan (JSON)

```json
{
  "scene": {
    "environment": "outer space",
    "lighting": "single sun lamp from the side",
    "time_of_day": "n/a",
    "atmosphere": "cinematic, dark void",
    "background_color": "#000005"
  },
  "objects": [
    {
      "name": "Earth",
      "type": "UV Sphere",
      "position": [0, 0, 0],
      "scale": [2, 2, 2],
      "material": {
        "color": "#2266AA",
        "type": "diffuse with procedural texture for continents",
        "roughness": 0.6
      }
    },
    {
      "name": "Stars",
      "type": "UV Sphere (large, inverted normals) with emissive dot texture",
      "position": [0, 0, 0],
      "scale": [50, 50, 50]
    }
  ],
  "motions": [
    {
      "object": "Earth",
      "keyframes": [
        { "frame": 1,   "rotation_euler_z": 0 },
        { "frame": 240, "rotation_euler_z": 360 }
      ],
      "interpolation": "linear"
    }
  ],
  "timeline": {
    "fps": 24,
    "duration_seconds": 10,
    "total_frames": 240
  },
  "camera": {
    "type": "static with slight orbit",
    "position": [6, -3, 2],
    "lens_mm": 85
  },
  "style": "cinematic",
  "render_settings": {
    "engine": "CYCLES",
    "samples": 256,
    "resolution": [1920, 1080],
    "output_format": "MP4"
  }
}
```

## Blender Python Script

See `rotating_earth.py` in the outputs directory.

## How to Run

```bash
# Install Blender (macOS)
brew install --cask blender

# Run headless
blender --background --python rotating_earth.py

# Run and render
blender --background --python rotating_earth.py -- --render
```

Output: `/tmp/rotating_earth_output.mp4`
