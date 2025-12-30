"""
Simple test to verify karaoke functionality.
"""

from karaoke import generate_karaoke_video
from karaoke.timing import create_word_timings, WordTiming
from karaoke.text_layout import TextLayout
from karaoke.utils import map_in_range, parse_text_style
import os


def test_utils():
    """Test utility functions."""
    print("Testing utilities...")
    
    # Test map_in_range
    result = map_in_range(5, 0, 10, 0, 100)
    assert result == 50, f"Expected 50, got {result}"
    
    result = map_in_range(15, 0, 10, 0, 100, constrain=True)
    assert result == 100, f"Expected 100, got {result}"
    
    # Test parse_text_style
    styles = parse_text_style('bold italic uppercase')
    assert styles['bold'] == True
    assert styles['italic'] == True
    assert styles['uppercase'] == True
    
    print("✓ Utilities test passed")


def test_timing():
    """Test timing functionality."""
    print("Testing timing...")
    
    # Test WordTiming
    wt = WordTiming('hello', 0, 2)
    assert wt.get_progress(0) == 0
    assert wt.get_progress(1) == 50
    assert wt.get_progress(2) == 100
    assert wt.get_status(0) == 'active'
    assert wt.get_status(3) == 'passed'
    
    # Test create_word_timings
    timings = create_word_timings('hello world', 0, 4)
    assert len(timings) == 3  # 'hello', ' ', 'world'
    assert timings[0].text == 'hello'
    assert timings[1].text == ' '
    assert timings[2].text == 'world'
    
    print("✓ Timing test passed")


def test_text_layout():
    """Test text layout functionality."""
    print("Testing text layout...")
    
    layout = TextLayout(font_size=24)
    
    # Test measure_text
    width, height = layout.measure_text('hello')
    assert width > 0, "Width should be positive"
    assert height > 0, "Height should be positive"
    
    # Test measure_words
    words = ['hello', ' ', 'world']
    word_sizes = layout.measure_words(words)
    assert len(word_sizes) == 3
    assert word_sizes[0]['text'] == 'hello'
    assert word_sizes[0]['width'] > 0
    
    print("✓ Text layout test passed")


def test_video_generation():
    """Test video generation."""
    print("Testing video generation...")
    
    lyrics_data = [
        {
            'text': 'Test karaoke',
            'start_time': 0,
            'end_time': 2
        }
    ]
    
    output_path = '/tmp/test_karaoke.mp4'
    
    try:
        result = generate_karaoke_video(
            lyrics_data=lyrics_data,
            output_path=output_path,
            width=640,
            height=360,
            fps=10,  # Low FPS for faster test
            font_size=48
        )
        
        assert os.path.exists(output_path), "Video file should be created"
        assert os.path.getsize(output_path) > 0, "Video file should not be empty"
        
        print(f"✓ Video generated: {output_path}")
        print(f"  File size: {os.path.getsize(output_path)} bytes")
        
        # Clean up
        os.remove(output_path)
        print("✓ Video generation test passed")
        
    except Exception as e:
        print(f"✗ Video generation test failed: {e}")
        raise


def run_all_tests():
    """Run all tests."""
    print("=" * 50)
    print("Running Karaoke Module Tests")
    print("=" * 50)
    print()
    
    try:
        test_utils()
        test_timing()
        test_text_layout()
        test_video_generation()
        
        print()
        print("=" * 50)
        print("✓ All tests passed!")
        print("=" * 50)
        
    except Exception as e:
        print()
        print("=" * 50)
        print(f"✗ Tests failed: {e}")
        print("=" * 50)
        raise


if __name__ == '__main__':
    run_all_tests()
