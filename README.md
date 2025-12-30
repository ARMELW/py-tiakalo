# py-tiakalo

🎤 Python Karaoke Word Fill Effect - Generate karaoke-style videos with progressive word-by-word filling using OpenCV and Pillow.

## 📌 Overview

This project implements a karaoke word fill effect in Python, porting the functionality from React + SVG to Python + OpenCV. It generates MP4 videos with synchronized lyrics that fill progressively from left to right as each word becomes active.

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

## 🚀 Installation

```bash
pip install -r requirements.txt
```

### Requirements

- Python 3.10+
- OpenCV (`opencv-python`)
- Pillow (`PIL`)
- NumPy

## 📖 Usage

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
# Run all examples
python example.py

# Run specific example
python example.py simple
python example.py styled
python example.py multiline
```

## 🏗️ Architecture

```
karaoke/
├── __init__.py       # Module exports
├── main.py           # Video generation functions
├── renderer.py       # Frame-by-frame rendering
├── text_layout.py    # Word measurement with Pillow
├── timing.py         # Word timing calculations
└── utils.py          # Utility functions (mapInRange, etc.)
```

## 🎨 Customization

### Colors

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

### `generate_karaoke_video()`

Generate a karaoke video with all lyrics displayed as a single line.

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
