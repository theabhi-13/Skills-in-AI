# Rocket Launch Animation — With Skill Output

## Animation Plan (JSON)

```json
{
  "scene": {
    "environment": "outdoor launch pad",
    "lighting": "dramatic, warm key light with blue rim",
    "time_of_day": "dusk",
    "atmosphere": "cinematic",
    "background_color": "#1A1A2E"
  },
  "objects": [
    {
      "name": "Rocket",
      "type": "composite (cone + cylinder body + cylinder boosters)",
      "position": [0, 0, 0],
      "scale": [1, 1, 1],
      "material": { "color": "#DDDDDD", "type": "metallic", "roughness": 0.2 }
    },
    {
      "name": "Ground",
      "type": "Plane",
      "position": [0, 0, 0],
      "scale": [30, 30, 1],
      "material": { "color": "#3A3A3A", "type": "diffuse", "roughness": 0.95 }
    },
    {
      "name": "SmokeEmitter",
      "type": "Plane with particle system (smoke/fire)",
      "position": [0, 0, 0.1]
    }
  ],
  "motions": [
    {
      "object": "Rocket",
      "keyframes": [
        { "frame": 1,   "location": [0, 0, 0] },
        { "frame": 30,  "location": [0, 0, 0] },
        { "frame": 60,  "location": [0, 0, 2] },
        { "frame": 90,  "location": [0, 0, 8] },
        { "frame": 120, "location": [0, 0, 20] },
        { "frame": 160, "location": [0, 0, 50] },
        { "frame": 200, "location": [0, 0, 120] }
      ],
      "interpolation": "bezier (ease-in for acceleration)"
    }
  ],
  "timeline": {
    "fps": 24,
    "duration_seconds": 8.3,
    "total_frames": 200
  },
  "camera": {
    "type": "tracking (follows rocket upward)",
    "position": [15, -10, 3],
    "target": "Rocket",
    "lens_mm": 35
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

See `rocket_launch.py` in the outputs directory.

## How to Run

```bash
# Install Blender
brew install --cask blender

# Run headless
blender --background --python rocket_launch.py

# Render the animation
blender --background --python rocket_launch.py -- --render
```

Output: `/tmp/rocket_launch_output.mp4`
