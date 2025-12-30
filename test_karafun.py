"""
Test Karafun-style karaoke functionality.
"""

from karaoke import generate_karafun_video
from karaoke.karafun_renderer import KarafunRenderer
from karaoke.text_layout import TextLayout
import os


def test_karafun_renderer():
    """Test Karafun renderer initialization."""
    print("Testing Karafun renderer...")
    
    renderer = KarafunRenderer(width=640, height=360)
    
    # Check color scheme
    assert renderer.inactive_color == (255, 255, 255, 255), "Inactive color should be white"
    assert renderer.done_color == (237, 61, 234, 255), "Done color should be magenta/pink"
    
    print("✓ Karafun renderer test passed")


def test_karafun_video_generation():
    """Test Karafun video generation."""
    print("Testing Karafun video generation...")
    
    lyrics_data = [
        {
            'text': 'First line of karaoke',
            'start_time': 0,
            'end_time': 2
        },
        {
            'text': 'Second line follows',
            'start_time': 2,
            'end_time': 4
        }
    ]
    
    output_path = '/tmp/test_karafun.mp4'
    
    try:
        result = generate_karafun_video(
            lyrics_data=lyrics_data,
            output_path=output_path,
            width=640,
            height=360,
            fps=10,  # Low FPS for faster test
            font_size=36,
            title_duration=0  # No title screen for test
        )
        
        assert os.path.exists(output_path), "Video file should be created"
        assert os.path.getsize(output_path) > 0, "Video file should not be empty"
        
        print(f"✓ Video generated: {output_path}")
        print(f"  File size: {os.path.getsize(output_path)} bytes")
        
        # Clean up
        os.remove(output_path)
        print("✓ Karafun video generation test passed")
        
    except Exception as e:
        print(f"✗ Karafun video generation test failed: {e}")
        raise


def test_karafun_with_title():
    """Test Karafun video with title screen."""
    print("Testing Karafun video with title screen...")
    
    lyrics_data = [
        {
            'text': 'Test song lyrics',
            'start_time': 0,
            'end_time': 2
        }
    ]
    
    output_path = '/tmp/test_karafun_title.mp4'
    
    try:
        result = generate_karafun_video(
            lyrics_data=lyrics_data,
            output_path=output_path,
            width=640,
            height=360,
            fps=10,
            font_size=36,
            title_duration=1.0,  # 1 second title screen
            song_title='Test Song',
            artist_name='Test Artist'
        )
        
        assert os.path.exists(output_path), "Video file should be created"
        assert os.path.getsize(output_path) > 0, "Video file should not be empty"
        
        print(f"✓ Video with title generated: {output_path}")
        print(f"  File size: {os.path.getsize(output_path)} bytes")
        
        # Clean up
        os.remove(output_path)
        print("✓ Karafun video with title test passed")
        
    except Exception as e:
        print(f"✗ Karafun video with title test failed: {e}")
        raise


def run_all_tests():
    """Run all Karafun tests."""
    print("=" * 50)
    print("Running Karafun Karaoke Tests")
    print("=" * 50)
    print()
    
    try:
        test_karafun_renderer()
        test_karafun_video_generation()
        test_karafun_with_title()
        
        print()
        print("=" * 50)
        print("✓ All Karafun tests passed!")
        print("=" * 50)
        
    except Exception as e:
        print()
        print("=" * 50)
        print(f"✗ Tests failed: {e}")
        print("=" * 50)
        raise


if __name__ == '__main__':
    run_all_tests()
