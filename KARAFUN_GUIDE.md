# Karafun Style Karaoke - Usage Guide

## Overview

The Karafun-style karaoke renderer provides a professional karaoke experience inspired by popular karaoke systems. It features:

- **Two-line display**: Shows current and next line simultaneously
- **Professional color scheme**: White text that turns magenta/pink as words are sung
- **Progressive fill**: Smooth word-by-word filling animation
- **Title screen**: Optional intro screen with song title and artist
- **Header**: Optional branding header with site name and status

## Quick Start

```python
from karaoke import generate_karafun_video

# Simple lyrics data
lyrics_data = [
    {'text': 'First line of your song', 'start_time': 0, 'end_time': 2},
    {'text': 'Second line follows here', 'start_time': 2, 'end_time': 4},
    {'text': 'And so on...', 'start_time': 4, 'end_time': 6}
]

# Generate video
generate_karafun_video(
    lyrics_data=lyrics_data,
    output_path='my_karaoke.mp4',
    song_title='Song Title',
    artist_name='Artist Name'
)
```

## Features Explained

### Two-Line Display

The Karafun renderer displays two lines at once:
- **Upper line**: The currently singing line (highlighted as you sing)
- **Lower line**: The next line (fades in gradually for preparation)

This gives singers time to prepare for the next line while focusing on the current one.

### Color Scheme

The color scheme is fixed to match professional karaoke standards:

1. **White (255, 255, 255)**: Unsung words waiting to be sung
2. **Magenta/Pink (237, 61, 234)**: Words that have been sung
3. **Progressive fill**: Active word fills from white to magenta as you sing

### Title Screen

Enable the title screen to display song information before lyrics start:

```python
generate_karafun_video(
    lyrics_data=lyrics_data,
    title_duration=3.0,  # 3 seconds of title screen
    song_title='My Favorite Song',
    artist_name='Famous Artist'
)
```

The title screen features:
- Large, centered song title with glow effect
- Artist name below in italics
- Decorative underline
- Smooth fade to lyrics

### Header

The header appears at the top of the screen during lyrics display:

```python
generate_karafun_video(
    lyrics_data=lyrics_data,
    show_header=True  # Enable header (default)
)
```

Header includes:
- Site name: "tiakalo.org" on the left
- Status indicator: "♪ KARAOKE" on the right
- Decorative top line in magenta

To hide the header:

```python
generate_karafun_video(
    lyrics_data=lyrics_data,
    show_header=False  # Hide header
)
```

## Customization Options

### Video Dimensions

```python
generate_karafun_video(
    lyrics_data=lyrics_data,
    width=1920,    # Full HD width
    height=1080,   # Full HD height
    fps=60         # Smooth 60 FPS
)
```

Recommended resolutions:
- **HD**: 1280x720
- **Full HD**: 1920x1080
- **4K**: 3840x2160

### Font Settings

```python
generate_karafun_video(
    lyrics_data=lyrics_data,
    font_size=60,           # Larger text
    style='bold',           # Bold style (recommended)
    font_family='/path/to/custom.ttf'  # Custom font
)
```

Font size recommendations:
- **Small screens (720p)**: 48-52px
- **Medium screens (1080p)**: 52-60px
- **Large screens (4K)**: 80-100px

### Background Color

```python
generate_karafun_video(
    lyrics_data=lyrics_data,
    bg_color=(10, 10, 30)  # Dark blue background
)
```

Popular background colors:
- **Black**: `(0, 0, 0)` - Classic karaoke
- **Dark Blue**: `(10, 10, 30)` - Modern look
- **Dark Purple**: `(20, 0, 40)` - Artistic feel
- **Dark Green**: `(0, 20, 10)` - Nature theme

### Disable Title Screen

```python
generate_karafun_video(
    lyrics_data=lyrics_data,
    title_duration=0  # No title screen
)
```

## Advanced Usage

### Timing Optimization

For best results, ensure your timing data is accurate:

```python
lyrics_data = [
    {
        'text': 'Hello world',
        'start_time': 0.0,      # Precise start time
        'end_time': 2.5         # Precise end time
    },
    {
        'text': 'How are you',
        'start_time': 2.5,      # Start immediately after previous
        'end_time': 5.0
    }
]
```

Tips:
- Use precise decimal timing (e.g., 2.5, not just 3)
- Avoid gaps between lines (start_time of line N = end_time of line N-1)
- Match timing to the actual singing duration

### Long Songs

For songs with many lines, the function handles everything automatically:

```python
# 50 lines of lyrics
lyrics_data = [
    {'text': f'Line {i+1} of the song', 'start_time': i*2, 'end_time': (i+1)*2}
    for i in range(50)
]

generate_karafun_video(
    lyrics_data=lyrics_data,
    output_path='long_song.mp4',
    fps=30  # Lower FPS for faster rendering of long videos
)
```

### Custom Branding

To customize the header branding, modify the site name in `karaoke/karafun_renderer.py`:

```python
# In _render_header method, change:
site_name = "tiakalo.org"
# To your custom name:
site_name = "YourSite.com"
```

## Comparison with Classic Style

| Feature | Karafun Style | Classic Style |
|---------|--------------|---------------|
| Lines displayed | 2 (current + next) | 1 (current only) |
| Color scheme | White → Magenta | Customizable |
| Header | Optional | No |
| Title screen | Optional | No |
| Use case | Professional karaoke | Simple demonstrations |

## Examples

### Example 1: Full Featured

```python
generate_karafun_video(
    lyrics_data=lyrics_data,
    output_path='full_featured.mp4',
    width=1920,
    height=1080,
    fps=30,
    font_size=60,
    style='bold',
    bg_color=(10, 10, 30),
    show_header=True,
    title_duration=4.0,
    song_title='Amazing Grace',
    artist_name='Traditional'
)
```

### Example 2: Minimal

```python
generate_karafun_video(
    lyrics_data=lyrics_data,
    output_path='minimal.mp4',
    show_header=False,
    title_duration=0
)
```

### Example 3: Custom Style

```python
generate_karafun_video(
    lyrics_data=lyrics_data,
    output_path='custom.mp4',
    width=1280,
    height=720,
    font_size=56,
    bg_color=(5, 5, 15),
    title_duration=3.0,
    song_title='🎵 My Custom Song 🎵',
    artist_name='⭐ Star Artist ⭐'
)
```

## Troubleshooting

### Font Issues

If text doesn't display correctly:
1. Check that system fonts are installed
2. Specify a custom TTF font path
3. The system will fall back to default font if needed

### Performance

For faster rendering:
- Reduce FPS (e.g., 24 or 25 instead of 30)
- Use lower resolution for testing
- Reduce font size slightly

### Video Size

Generated videos can be large. To reduce size:
- Use H.264 codec (requires additional setup)
- Reduce resolution
- Reduce FPS
- Shorten title_duration

## Next Steps

1. Try the example files: `python example_karafun.py`
2. Customize for your needs
3. Create your own karaoke videos!

For more information, see the main README.md file.
