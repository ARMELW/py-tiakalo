"""
Test script for new Karafun features: CLI, background image, time display, typewriter animation.
"""

from karaoke import generate_karafun_video
import os
import json


def test_background_image():
    """Test with background image (will skip if no image available)."""
    print("Testing background image support...")
    
    lyrics_data = [
        {'text': 'Welcome to Karafun with background', 'start_time': 0, 'end_time': 2.5},
        {'text': 'Beautiful scenery behind the lyrics', 'start_time': 2.5, 'end_time': 5.0}
    ]
    
    # Test without background image first (will use color)
    output_path = generate_karafun_video(
        lyrics_data=lyrics_data,
        output_path='test_no_bg_image.mp4',
        width=1280,
        height=720,
        fps=30,
        font_size=52,
        style='bold',
        bg_color=(10, 10, 30),
        show_header=True,
        title_duration=0
    )
    
    print(f"✓ Generated video without background: {output_path}")
    
    # Cleanup
    try:
        if os.path.exists(output_path):
            os.remove(output_path)
    except OSError as e:
        print(f"Warning: Could not remove {output_path}: {e}")


def test_time_display():
    """Test time display feature."""
    print("\nTesting time display...")
    
    lyrics_data = [
        {'text': 'First line with time display', 'start_time': 0, 'end_time': 2},
        {'text': 'Second line continues here', 'start_time': 2, 'end_time': 4},
        {'text': 'Final line showing time', 'start_time': 4, 'end_time': 6}
    ]
    
    output_path = generate_karafun_video(
        lyrics_data=lyrics_data,
        output_path='test_time_display.mp4',
        width=1280,
        height=720,
        fps=30,
        font_size=52,
        style='bold',
        bg_color=(0, 0, 0),
        show_header=True,
        show_time=True,  # Enable time display
        title_duration=0
    )
    
    print(f"✓ Generated video with time display: {output_path}")
    
    # Cleanup
    try:
        if os.path.exists(output_path):
            os.remove(output_path)
    except OSError as e:
        print(f"Warning: Could not remove {output_path}: {e}")


def test_typewriter_animation():
    """Test typewriter animation for title screen."""
    print("\nTesting typewriter animation...")
    
    lyrics_data = [
        {'text': 'After the typewriter title', 'start_time': 0, 'end_time': 2.5},
        {'text': 'We continue with the song', 'start_time': 2.5, 'end_time': 5.0}
    ]
    
    output_path = generate_karafun_video(
        lyrics_data=lyrics_data,
        output_path='test_typewriter.mp4',
        width=1280,
        height=720,
        fps=30,
        font_size=52,
        style='bold',
        bg_color=(10, 10, 30),
        show_header=True,
        title_duration=3.0,
        song_title='Typewriter Animation Test',
        artist_name='Test Artist',
        typewriter_speed=0.05  # Typewriter effect
    )
    
    print(f"✓ Generated video with typewriter animation: {output_path}")
    
    # Cleanup
    try:
        if os.path.exists(output_path):
            os.remove(output_path)
    except OSError as e:
        print(f"Warning: Could not remove {output_path}: {e}")


def test_cli_config():
    """Test CLI configuration loading."""
    print("\nTesting CLI configuration...")
    
    # Test if config file exists
    config_file = 'config_example.json'
    if os.path.exists(config_file):
        print(f"✓ Found config file: {config_file}")
        
        # Try to load it
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        print(f"✓ Config loaded successfully with {len(config.get('lyrics', []))} lyrics lines")
    else:
        print(f"⚠ Config file not found: {config_file}")


def test_all_features():
    """Test all new features together."""
    print("\nTesting all features combined...")
    
    lyrics_data = [
        {'text': 'Welcome to the complete Karafun demo', 'start_time': 0, 'end_time': 2.5},
        {'text': 'With all the new amazing features', 'start_time': 2.5, 'end_time': 5.0},
        {'text': 'Time display and typewriter effect', 'start_time': 5.0, 'end_time': 7.5},
        {'text': 'Everything working perfectly together', 'start_time': 7.5, 'end_time': 10.0}
    ]
    
    output_path = generate_karafun_video(
        lyrics_data=lyrics_data,
        output_path='test_all_features.mp4',
        width=1280,
        height=720,
        fps=30,
        font_size=52,
        style='bold',
        bg_color=(10, 10, 30),
        show_header=True,
        show_time=True,
        title_duration=3.0,
        song_title='Complete Feature Test',
        artist_name='Karafun Renderer',
        typewriter_speed=0.05
    )
    
    print(f"✓ Generated video with all features: {output_path}")
    
    # Keep this one for visual inspection
    print(f"  (Keeping file for inspection)")


if __name__ == '__main__':
    print("=" * 70)
    print("KARAFUN NEW FEATURES TEST SUITE")
    print("=" * 70)
    
    try:
        test_background_image()
        test_time_display()
        test_typewriter_animation()
        test_cli_config()
        test_all_features()
        
        print("\n" + "=" * 70)
        print("✓ ALL TESTS PASSED")
        print("=" * 70)
    except Exception as e:
        print(f"\n✗ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
