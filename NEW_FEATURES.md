# Karafun-like Rendering Features

## Overview

This document describes the new Karafun-like rendering features added to py-tiakalo, including typewriter animation, time display, background image support, and CLI configuration.

## New Features

### 1. Background Image Support

You can now set a custom background image for your karaoke videos instead of just a solid color.

**Usage:**

```python
generate_karafun_video(
    lyrics_data=lyrics_data,
    bg_image='/path/to/background.jpg',  # Path to your image
    bg_color=(0, 0, 0),  # Fallback color if image fails to load
    output_path='karaoke.mp4'
)
```

**Supported formats:** JPG, PNG, BMP, and other formats supported by Pillow

**Note:** The image will be automatically resized to match your video dimensions.

### 2. Typewriter Animation for Title & Artist

The title screen now features a typewriter animation where the title appears letter by letter, followed by a progressive underline animation from left to right.

**How it works:**
- Title text appears character by character
- Once complete, an underline animates from left to right
- Artist name then appears with typewriter effect
- Speed is configurable

**Usage:**

```python
generate_karafun_video(
    lyrics_data=lyrics_data,
    song_title='My Song',
    artist_name='My Artist',
    title_duration=4.0,  # Duration of title screen
    typewriter_speed=0.05,  # Seconds per character (default: 0.05)
    output_path='karaoke.mp4'
)
```

**Customization:**
- `typewriter_speed`: Lower values = faster typing (e.g., 0.03 for fast, 0.08 for slow)
- Title appears first, then underline animates, then artist appears

### 3. Time Display

Display remaining time during karaoke playback. Shows different formats based on state:

**When singing:**
- Shows short format: `MM:SS` (e.g., `02:15`)

**When waiting (before lyrics or between gaps):**
- Shows long format: `Remaining: MM:SS` (e.g., `Remaining: 03:45`)

**Usage:**

```python
generate_karafun_video(
    lyrics_data=lyrics_data,
    show_time=True,  # Enable time display
    output_path='karaoke.mp4'
)
```

**Display location:** Bottom-right corner with semi-transparent background

### 4. CLI Configuration Support

Generate videos using JSON configuration files for easier management and repeatability.

**Basic Usage:**

```bash
# Generate from config file
python -m karaoke.cli --config my_config.json

# Override output path
python -m karaoke.cli --config my_config.json --output custom_output.mp4
```

**Configuration File Structure:**

```json
{
  "output_path": "karaoke_video.mp4",
  "video": {
    "width": 1280,
    "height": 720,
    "fps": 30
  },
  "background": {
    "color": [10, 10, 30],
    "image": "/path/to/background.jpg"
  },
  "font": {
    "family": "Arial",
    "size": 52,
    "style": "bold"
  },
  "title": {
    "song": "Song Title",
    "artist": "Artist Name",
    "duration": 4.0
  },
  "animation": {
    "show_header": true,
    "typewriter_speed": 0.05
  },
  "display": {
    "show_time": true
  },
  "lyrics": [
    {
      "text": "First line of lyrics",
      "start_time": 0,
      "end_time": 3
    },
    {
      "text": "Second line continues",
      "start_time": 3,
      "end_time": 6
    }
  ]
}
```

**Configuration Fields:**

- `output_path`: Where to save the video
- `video`: Video settings (width, height, fps)
- `background`: Background color (RGB array) and optional image path
- `font`: Font settings (family, size, style)
- `title`: Title screen settings (song, artist, duration)
- `animation`: Animation settings (show_header, typewriter_speed)
- `display`: Display settings (show_time)
- `lyrics`: Array of lyric objects with text and timing

### 5. Alternating Sliding Lyrics (Two-Line Viewport)

The karaoke renderer displays two lines simultaneously with alternating slide behavior:

**How it works:**
1. Two lines are always visible (current + next)
2. Lines slide in/out alternately (not in pairs)
3. When one line ends, it slides out and is replaced by a new line
4. The other line continues playing
5. This creates a smooth, continuous flow

**Visual Example:**

```
t=0-3s:
  Line A: "Welcome to the Karafun style karaoke" (animating)
  Line B: "Watch the words turn magenta as you sing" (animating)

t=3s (Line A ends):
  Line A slides out ← "Two lines displayed at the same time" slides in
  Line B continues: "Watch the words turn magenta as you sing" (still animating)

t=6s (Line B ends):
  Line A continues: "Two lines displayed at the same time" (still animating)
  Line B slides out ← "With a beautiful header and title screen" slides in
```

**Key Features:**
- Only one line changes at a time
- No waiting for both lines to finish
- Always exactly 2 lines visible
- Smooth alternating transitions
- Professional Karafun-style appearance

## Complete Example

Here's a complete example using all new features:

```python
from karaoke import generate_karafun_video

lyrics_data = [
    {'text': 'Welcome to our karaoke night', 'start_time': 0, 'end_time': 2.5},
    {'text': 'Sing along with confidence', 'start_time': 2.5, 'end_time': 5.0},
    {'text': 'Watch the magic unfold', 'start_time': 5.0, 'end_time': 7.5},
    {'text': 'As the words light up', 'start_time': 7.5, 'end_time': 10.0},
]

generate_karafun_video(
    lyrics_data=lyrics_data,
    output_path='complete_demo.mp4',
    
    # Video settings
    width=1280,
    height=720,
    fps=30,
    
    # Background
    bg_color=(10, 10, 30),  # Dark blue
    bg_image='/path/to/background.jpg',  # Optional
    
    # Font
    font_size=52,
    font_family='Arial',
    style='bold',
    
    # Title screen with animation
    song_title='Amazing Song',
    artist_name='Talented Artist',
    title_duration=4.0,
    typewriter_speed=0.05,
    
    # Display options
    show_header=True,
    show_time=True,
)
```

## CLI Example

Create a config file `my_song.json`:

```json
{
  "output_path": "my_song_karaoke.mp4",
  "video": {"width": 1920, "height": 1080, "fps": 30},
  "background": {
    "color": [15, 15, 40],
    "image": "backgrounds/sunset.jpg"
  },
  "font": {"family": "Arial", "size": 60, "style": "bold"},
  "title": {
    "song": "My Favorite Song",
    "artist": "Famous Singer",
    "duration": 5.0
  },
  "animation": {
    "show_header": true,
    "typewriter_speed": 0.04
  },
  "display": {"show_time": true},
  "lyrics": [
    {"text": "First verse line one", "start_time": 0, "end_time": 3},
    {"text": "First verse line two", "start_time": 3, "end_time": 6}
  ]
}
```

Generate the video:

```bash
python -m karaoke.cli --config my_song.json
```

## Visual Accuracy

All features are designed to match the Karafun-style karaoke appearance as closely as possible:

✅ **Header:** Professional header with site name and status indicator
✅ **Time Display:** Clean, readable time counter in bottom-right
✅ **Typewriter Effect:** Smooth character-by-character title animation
✅ **Progressive Underline:** Animated underline following title completion
✅ **Two-Line Display:** Alternating slide transitions for continuous flow
✅ **Color Scheme:** White → Magenta word highlighting
✅ **Layout:** Centered, professional spacing matching Karafun standards

## Performance Tips

- **Background Images:** Use images close to your video resolution for best performance
- **Typewriter Speed:** 0.05 seconds per character is optimal for readability
- **FPS:** 30 FPS provides smooth animation without excessive file size
- **Title Duration:** 3-5 seconds is ideal for title screen visibility

## Troubleshooting

**Background image not showing:**
- Verify the image path is correct
- Ensure the image format is supported (JPG, PNG)
- Check file permissions

**Typewriter animation too fast/slow:**
- Adjust `typewriter_speed` parameter
- Try values between 0.03 (fast) and 0.08 (slow)

**Time not displaying:**
- Ensure `show_time=True` is set
- Check that you're not in title screen mode

**CLI config not loading:**
- Verify JSON syntax is valid
- Check all required fields are present
- Ensure lyrics array has valid timing data

## Migration from Previous Version

If you're upgrading from a previous version, all existing code continues to work. New parameters are optional:

```python
# Old code still works
generate_karafun_video(
    lyrics_data=lyrics_data,
    output_path='video.mp4'
)

# Add new features when ready
generate_karafun_video(
    lyrics_data=lyrics_data,
    output_path='video.mp4',
    show_time=True,  # NEW
    bg_image='bg.jpg',  # NEW
    typewriter_speed=0.05  # NEW
)
```

## See Also

- [Main README](README.md) - General usage and installation
- [Karafun Guide](KARAFUN_GUIDE.md) - Detailed Karafun renderer documentation
- [config_example.json](config_example.json) - Example configuration file
- [example_complete_features.py](example_complete_features.py) - Complete example script
