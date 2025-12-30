"""
Test the refactored features:
1. Transparent header (no black bar)
2. Time display with "Remaining:" prefix during pauses
3. Skip title when lyrics start early
"""

from karaoke import generate_karafun_video


def test_transparent_header_with_time():
    """Test transparent header and time display."""
    lyrics_data = [
        {
            'text': 'First line with some lyrics here',
            'start_time': 0,
            'end_time': 3
        },
        {
            'text': 'Second line after a pause',
            'start_time': 6,  # 3 second pause
            'end_time': 9
        },
        {
            'text': 'Third line continues',
            'start_time': 9,
            'end_time': 12
        }
    ]
    
    print("Generating video with transparent header and time display...")
    output_path = generate_karafun_video(
        lyrics_data=lyrics_data,
        output_path='test_transparent_header.mp4',
        width=1280,
        height=720,
        fps=30,
        font_size=52,
        style='bold',
        bg_color=(10, 10, 30),  # Dark blue background
        show_header=True,
        show_time=True,  # Enable time display
        title_duration=3.0,
        song_title='Test Song',
        artist_name='Test Artist'
    )
    print(f"Video generated: {output_path}")


def test_skip_title_early_lyrics():
    """Test skipping title when lyrics start too early."""
    lyrics_data = [
        {
            'text': 'Lyrics start immediately',
            'start_time': 0,  # Starts at 0, should skip title
            'end_time': 2
        },
        {
            'text': 'Second line follows',
            'start_time': 2,
            'end_time': 4
        }
    ]
    
    print("\nGenerating video with early lyrics (should skip title)...")
    output_path = generate_karafun_video(
        lyrics_data=lyrics_data,
        output_path='test_skip_title.mp4',
        width=1280,
        height=720,
        fps=30,
        font_size=52,
        style='bold',
        bg_color=(10, 10, 30),
        show_header=True,
        title_duration=3.0,  # Title requested but should be skipped
        song_title='Should Be Skipped',
        artist_name='Test Artist'
    )
    print(f"Video generated: {output_path}")


def test_normal_title():
    """Test normal title screen when lyrics start late enough."""
    lyrics_data = [
        {
            'text': 'Lyrics start after title duration',
            'start_time': 5,  # Starts late, title should show
            'end_time': 8
        },
        {
            'text': 'Second line continues',
            'start_time': 8,
            'end_time': 11
        }
    ]
    
    print("\nGenerating video with normal title (lyrics start late)...")
    output_path = generate_karafun_video(
        lyrics_data=lyrics_data,
        output_path='test_normal_title.mp4',
        width=1280,
        height=720,
        fps=30,
        font_size=52,
        style='bold',
        bg_color=(10, 10, 30),
        show_header=True,
        title_duration=3.0,
        song_title='Normal Title',
        artist_name='Test Artist'
    )
    print(f"Video generated: {output_path}")


if __name__ == '__main__':
    test_transparent_header_with_time()
    test_skip_title_early_lyrics()
    test_normal_title()
    print("\nAll tests completed!")
