"""
Comprehensive example showcasing all refactored features:
1. Transparent header
2. Time display with "Remaining:" during pauses
3. Dark overlay on background image
4. Skip title when lyrics start early
5. Audio support with synchronization
"""

from karaoke import generate_karafun_video
import json


def create_config_with_audio():
    """Create a comprehensive config file with audio."""
    config = {
        "output_path": "final_demo.mp4",
        "video": {
            "width": 1280,
            "height": 720,
            "fps": 30
        },
        "background": {
            "color": [10, 10, 30],
            "image": "bg.jpg"
        },
        "font": {
            "family": "./Shantell.ttf",
            "size": 52,
            "style": "bold"
        },
        "title": {
            "song": "Comprehensive Demo",
            "artist": "tiakalo.org",
            "duration": 3.0
        },
        "animation": {
            "show_header": True,
            "typewriter_speed": 0.05
        },
        "display": {
            "show_time": True
        },
        "audio": {
            "path": "test_audio.mp3",
            "offset": 0.0
        },
        "lyrics": [
            {
                "text": "Transparent header with no black bar",
                "start_time": 0,
                "end_time": 3
            },
            {
                "text": "Dark overlay improves text visibility",
                "start_time": 3,
                "end_time": 6
            },
            {
                "text": "Time display during singing",
                "start_time": 6,
                "end_time": 8.5
            },
            {
                "text": "Remaining time shown during pause",
                "start_time": 11,
                "end_time": 14
            },
            {
                "text": "Audio synchronized with lyrics",
                "start_time": 14,
                "end_time": 17
            }
        ]
    }
    
    with open('demo_config_audio.json', 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print("✓ Config file created: demo_config_audio.json")
    return config


def generate_from_code():
    """Generate video directly from Python code with all features."""
    import os
    
    # Check if required files exist
    bg_image = 'bg.jpg' if os.path.exists('bg.jpg') else None
    audio_file = 'test_audio.mp3' if os.path.exists('test_audio.mp3') else None
    
    if not bg_image:
        print("Warning: bg.jpg not found, using solid color background")
    if not audio_file:
        print("Warning: test_audio.mp3 not found, generating video without audio")
    
    lyrics_data = [
        {
            'text': 'All features demonstrated here',
            'start_time': 0,
            'end_time': 3
        },
        {
            'text': 'Transparent header at the top',
            'start_time': 3,
            'end_time': 6
        },
        {
            'text': 'Background image with overlay',
            'start_time': 6,
            'end_time': 9
        },
        {
            'text': 'Watch for the pause...',
            'start_time': 9,
            'end_time': 11
        },
        {
            'text': 'Remaining time was shown!',
            'start_time': 14,
            'end_time': 17
        }
    ]
    
    print("\nGenerating video from Python code...")
    output_path = generate_karafun_video(
        lyrics_data=lyrics_data,
        output_path='demo_from_code.mp4',
        width=1280,
        height=720,
        fps=30,
        font_family='./Shantell.ttf' if os.path.exists('./Shantell.ttf') else 'Arial',
        font_size=52,
        style='bold',
        bg_color=(10, 10, 30),
        bg_image=bg_image,
        show_header=True,
        show_time=True,
        title_duration=2.5,
        song_title='Python API Demo',
        artist_name='tiakalo.org',
        typewriter_speed=0.05,
        audio_path=audio_file,
        audio_offset=0.0
    )
    print(f"✓ Video generated: {output_path}")


if __name__ == '__main__':
    print("=" * 60)
    print("COMPREHENSIVE FEATURE DEMONSTRATION")
    print("=" * 60)
    print("\nFeatures showcased:")
    print("  ✓ Transparent header (no black background)")
    print("  ✓ Dark overlay on background image")
    print("  ✓ Time display with 'Remaining:' during pauses")
    print("  ✓ Simple time format during singing")
    print("  ✓ Audio synchronization")
    print("  ✓ Title screen with typewriter animation")
    print()
    
    # Create config and generate
    config = create_config_with_audio()
    
    # Generate from Python code
    generate_from_code()
    
    print("\n" + "=" * 60)
    print("✅ All demonstrations completed successfully!")
    print("=" * 60)
    print("\nGenerated files:")
    print("  • demo_config_audio.json (config file)")
    print("  • demo_from_code.mp4 (video from Python API)")
    print("\nTo generate from config file:")
    print("  python -m karaoke.cli --config demo_config_audio.json")
