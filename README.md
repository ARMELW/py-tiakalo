# py-tiakalo

🎤 Python Karaoke Word Fill Effect - Generate karaoke-style videos with progressive word-by-word filling using OpenCV and Pillow.

## 📌 Overview

This project implements a karaoke word fill effect in Python, porting the functionality from React + SVG to Python + OpenCV. It generates MP4 videos with synchronized lyrics that fill progressively from left to right as each word becomes active.

## 🎬 Preview

**Karafun-Style Karaoke in Action:**

![Karafun Karaoke Screenshot](https://github.com/user-attachments/assets/c6fbebec-44c4-4894-ae1f-7eefdfeec2f4)

*Two-line display with white text turning magenta as words are sung, professional header, and centered layout.*

## ✨ Features

- ✅ Word-by-word text splitting
- ✅ Precise word timing (start/end times)
- ✅ Accurate word width measurement using Pillow
- ✅ Progressive fill calculation based on current time
- ✅ Three word states: inactive (gray), active (filling), passed (full color)
- ✅ MP4 video generation with OpenCV
- ✅ Support for font family, size, and styles (bold, italic, uppercase)
- ✅ Customizable colors for active/inactive states
- ✅ Multiple line support
- ✅ **Karafun-style renderer** with two-line display
- ✅ Title screen with song name and artist
- ✅ Header with site branding and status
- ✅ **NEW: Typewriter animation** for title screen with progressive underline
- ✅ **NEW: Time remaining display** (shows remaining time during playback)
- ✅ **NEW: Background image support** (use custom images as backgrounds)
- ✅ **NEW: Dark overlay** on background images to improve text visibility
- ✅ **NEW: CLI with JSON config** (generate videos from configuration files)
- ✅ **NEW: Audio support** (add audio tracks to karaoke videos with offset control)

## 🚀 Installation

```bash
pip install -r requirements.txt
```

**Note:** Audio support requires `ffmpeg` to be installed on your system:
```bash
# Ubuntu/Debian
sudo apt-get install ffmpeg

# macOS
brew install ffmpeg

# Windows
# Download from https://ffmpeg.org/download.html
```

### Requirements

- Python 3.10+
- OpenCV (`opencv-python`)
- Pillow (`PIL`)
- NumPy

## 📖 Usage

### Karafun Style (Recommended)

The Karafun style provides a professional karaoke experience with two lines displayed simultaneously, magenta highlighting for sung words, optional title screen with typewriter animation, time display, and background image support.

```python
from karaoke import generate_karafun_video

lyrics_data = [
    {
        'text': 'Welcome to the Karafun style karaoke',
        'start_time': 0,
        'end_time': 3
    },
    {
        'text': 'Watch the words turn magenta as you sing',
        'start_time': 3,
        'end_time': 6
    }
]

generate_karafun_video(
    lyrics_data=lyrics_data,
    output_path='karafun_demo.mp4',
    width=1280,
    height=720,
    fps=30,
    font_size=52,
    style='bold',
    bg_color=(10, 10, 30),  # Dark blue background
    bg_image=None,  # Optional: Path to background image
    show_header=True,
    show_time=True,  # Show time remaining display
    title_duration=3.0,
    song_title='My Karaoke Song',
    artist_name='Artist Name',
    typewriter_speed=0.05,  # Typewriter animation speed
    audio_path='song.mp3',  # Optional: Add audio track
    audio_offset=0.0  # Optional: Audio offset in seconds
)
```

### Adding Audio (NEW)

You can add audio tracks to your karaoke videos:

```python
generate_karafun_video(
    lyrics_data=lyrics_data,
    output_path='karaoke_with_audio.mp4',
    audio_path='background_music.mp3',  # Path to audio file
    audio_offset=0.5,  # Delay audio by 0.5 seconds
    # ... other parameters
)
```

**Supported audio formats:** MP3, WAV, AAC, OGG, FLAC (any format supported by ffmpeg)

### CLI Configuration (NEW)

Generate videos using JSON configuration files:

```bash
# Generate video from config file
python -m karaoke.cli --config config.json

# Specify custom output path
python -m karaoke.cli --config config.json --output my_video.mp4
```

**Example config.json:**
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
    "image": null
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
  "audio": {
    "path": "song.mp3",
    "offset": 0.0
  },
  "lyrics": [
    {"text": "First line", "start_time": 0, "end_time": 3},
    {"text": "Second line", "start_time": 3, "end_time": 6}
  ]
}
```

### Basic Example

```python
from karaoke import generate_karaoke_video

lyrics_data = [
    {
        'text': 'Hello world this is karaoke',
        'start_time': 0,
        'end_time': 3
    },
    {
        'text': 'Watch the words fill in',
        'start_time': 3,
        'end_time': 6
    }
]

generate_karaoke_video(
    lyrics_data=lyrics_data,
    output_path='output.mp4',
    width=1280,
    height=720,
    fps=30,
    font_size=60,
    active_color=(255, 69, 0),  # Orange-red
    inactive_color=(136, 136, 136),  # Gray
    bg_color=(0, 0, 0)  # Black
)
```

### Run Examples

```bash
# Run Karafun-style examples
python example_karafun.py
python example_karafun.py with_title
python example_karafun.py simple
python example_karafun.py no_header

# Run classic style examples
python example.py
python example.py simple
python example.py styled
python example.py multiline
```

## 🏗️ Architecture

```
karaoke/
├── __init__.py           # Module exports
├── main.py               # Video generation functions
├── renderer.py           # Classic frame-by-frame rendering
├── karafun_renderer.py   # Karafun-style two-line rendering
├── text_layout.py        # Word measurement with Pillow
├── timing.py             # Word timing calculations
└── utils.py              # Utility functions (mapInRange, etc.)
```

## 🎨 Customization

### Karafun Style Colors

The Karafun style uses a fixed color scheme inspired by professional karaoke systems:

```python
# Fixed Karafun colors (cannot be changed)
inactive_color = (255, 255, 255)  # White for unsung words
done_color = (237, 61, 234)       # Magenta/pink for sung words
bg_color = (0, 0, 0)              # Black or custom background
```

### Classic Style Colors

```python
active_color=(255, 69, 0)      # RGB for active/passed words
inactive_color=(136, 136, 136)  # RGB for inactive words
bg_color=(0, 0, 0)              # RGB for background
```

### Text Styles

```python
style='bold italic uppercase'  # Space-separated style options
font_size=48                    # Font size in pixels
font_family='Arial'             # Font name or path to TTF file
```

### Video Settings

```python
width=1280         # Video width in pixels
height=720         # Video height in pixels
fps=30             # Frames per second
```

## 🧩 API Reference

### `generate_karafun_video()`

Generate a professional Karafun-style karaoke video with two-line display.

**Features:**
- Two lines displayed simultaneously (current + next)
- White text for unsung words
- Magenta/pink highlighting for sung words
- Progressive word-by-word fill effect
- Optional header with site branding
- Optional title screen with song info
- **NEW:** Typewriter animation for title
- **NEW:** Time remaining display
- **NEW:** Background image support with dark overlay
- **NEW:** Audio track support

**Parameters:**
- `lyrics_data` (list): List of dictionaries with 'text', 'start_time', 'end_time'
- `output_path` (str): Path to output MP4 file
- `width` (int): Video width in pixels (default: 1280)
- `height` (int): Video height in pixels (default: 720)
- `fps` (int): Frames per second (default: 30)
- `font_family` (str): Font family name or TTF file path
- `font_size` (int): Font size in pixels (default: 48, recommend 48-60 for Karafun)
- `style` (str): Text style string (default: 'bold')
- `bg_color` (tuple): RGB color tuple for background (default: (0, 0, 0))
- `bg_image` (str): Path to background image file (optional, **NEW**)
- `show_header` (bool): Show header with branding (default: True)
- `show_time` (bool): Show time remaining display (default: False, **NEW**)
- `title_duration` (float): Duration of title screen in seconds (default: 3.0, 0 to disable)
- `song_title` (str): Song title for title screen (optional)
- `artist_name` (str): Artist name for title screen (optional)
- `typewriter_speed` (float): Speed of typewriter animation in seconds per character (default: 0.05, **NEW**)
- `audio_path` (str): Path to audio file to add to video (optional, **NEW**)
- `audio_offset` (float): Audio offset in seconds - positive delays audio, negative advances it (default: 0.0, **NEW**)
- `typewriter_speed` (float): Speed of typewriter animation in seconds per character (default: 0.05, **NEW**)

**Returns:** Path to the generated video file

### `generate_karaoke_video()`

Generate a karaoke video with all lyrics displayed as a single line (classic style).

**Parameters:**
- `lyrics_data` (list): List of dictionaries with 'text', 'start_time', 'end_time'
- `output_path` (str): Path to output MP4 file
- `width` (int): Video width in pixels
- `height` (int): Video height in pixels
- `fps` (int): Frames per second
- `font_family` (str): Font family name or TTF file path
- `font_size` (int): Font size in pixels
- `style` (str): Text style string (e.g., 'bold italic')
- `active_color` (tuple): RGB color tuple for active/passed text
- `inactive_color` (tuple): RGB color tuple for inactive text
- `bg_color` (tuple): RGB color tuple for background

**Returns:** Path to the generated video file

### `generate_karaoke_video_with_lines()`

Generate a karaoke video with multiple lines displayed.

Same parameters as `generate_karaoke_video()` plus:
- `line_spacing` (int): Spacing between lines in pixels

## 🎯 Implementation Details

### Progressive Fill Algorithm

1. Split text into words (preserving spaces)
2. Assign timing to each word
3. For each frame at time `t`:
   - Calculate word progress: `(t - start) / (end - start) * 100`
   - Determine word status: inactive, active, or passed
   - Render inactive words in gray
   - Render active word with clipped fill based on progress
   - Render passed words in full active color

### Word Measurement

Uses Pillow's `ImageFont` and `ImageDraw.textbbox()` to accurately measure word dimensions, ensuring precise progressive fill calculations.

### Video Generation

- Each frame is rendered as a PIL Image
- Text is drawn with Pillow for high-quality rendering
- Progressive fill uses alpha masking
- Frames are converted to OpenCV format (BGR) and written to MP4

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the MIT License.
