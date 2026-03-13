# Bouncing Ball Animation — With Skill Output

## Animation Plan (JSON)

```json
{
  "scene": {
    "environment": "indoor studio",
    "lighting": "three-point setup (sun + area fill + rim)",
    "time_of_day": "neutral",
    "atmosphere": "clean, semi-realistic",
    "background_color": "#D0D0D0"
  },
  "objects": [
    {
      "name": "Ball",
      "type": "UV Sphere",
      "position": [0, 0, 5],
      "scale": [1, 1, 1],
      "material": {
        "color": "#CC2222",
        "type": "glossy",
        "roughness": 0.35,
        "subsurface": 0.1
      }
    },
    {
      "name": "Floor",
      "type": "Plane",
      "position": [0, 0, 0],
      "scale": [15, 15, 1],
      "material": {
        "color": "#999999",
        "type": "diffuse",
        "roughness": 0.9
      }
    }
  ],
  "motions": [
    {
      "object": "Ball",
      "keyframes": [
        { "frame": 1,  "location": [0, 0, 5],   "scale": [1.0, 1.0, 1.0] },
        { "frame": 18, "location": [0, 0, 0.5], "scale": [1.3, 1.3, 0.6] },
        { "frame": 30, "location": [0, 0, 3.5], "scale": [0.85, 0.85, 1.2] },
        { "frame": 45, "location": [0, 0, 0.5], "scale": [1.2, 1.2, 0.7] },
        { "frame": 55, "location": [0, 0, 2.0], "scale": [0.9, 0.9, 1.1] },
        { "frame": 68, "location": [0, 0, 0.5], "scale": [1.1, 1.1, 0.85] },
        { "frame": 75, "location": [0, 0, 1.0], "scale": [1.0, 1.0, 1.0] },
        { "frame": 85, "location": [0, 0, 0.5], "scale": [1.0, 1.0, 1.0] }
      ],
      "interpolation": "bezier"
    }
  ],
  "timeline": {
    "fps": 24,
    "duration_seconds": 3.5,
    "total_frames": 85
  },
  "camera": {
    "type": "static",
    "position": [10, 0, 3],
    "rotation": [80, 0, 90],
    "lens_mm": 50
  },
  "style": "semi-realistic",
  "render_settings": {
    "engine": "CYCLES",
    "samples": 128,
    "resolution": [1920, 1080],
    "output_format": "MP4"
  }
}
```

## Blender Python Script

See `bouncing_ball.py` in the outputs directory.

## How to Run

```bash
# Make sure Blender is installed
blender --version

# If not installed (macOS):
brew install --cask blender

# Run the script (headless, no GUI):
blender --background --python bouncing_ball.py

# Run and render the animation:
blender --background --python bouncing_ball.py -- --render
```

The rendered animation will be saved to `/tmp/bouncing_ball_output.mp4`.
