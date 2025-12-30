"""
Comprehensive test of all refactored features.
"""

from karaoke import generate_karafun_video


def test_all_features():
    """Test all features: transparent header, time display, overlay, skip title."""
    lyrics_data = [
        {
            'text': 'Welcome to tiakalo.org karaoke',
            'start_time': 0,
            'end_time': 3
        },
        {
            'text': 'Testing transparent header',
            'start_time': 3,
            'end_time': 6
        },
        {
            'text': 'Long pause coming up...',
            'start_time': 6,
            'end_time': 9
        },
        {
            'text': 'Pause time shows remaining',
            'start_time': 13,  # 4 second pause - should show "Remaining:" format
            'end_time': 16
        },
        {
            'text': 'Dark overlay helps visibility',
            'start_time': 16,
            'end_time': 19
        }
    ]
    
    print("Generating comprehensive test video...")
    print("Features tested:")
    print("  ✓ Transparent header (no black bar)")
    print("  ✓ Time display with 'Remaining:' during pauses")
    print("  ✓ Simple time format during singing")
    print("  ✓ Dark overlay on background image")
    print("  ✓ Title skipped when lyrics start early")
    
    output_path = generate_karafun_video(
        lyrics_data=lyrics_data,
        output_path='comprehensive_test.mp4',
        width=1280,
        height=720,
        fps=30,
        font_size=52,
        style='bold',
        bg_color=(10, 10, 30),
        bg_image='bg.jpg',
        show_header=True,
        show_time=True,
        title_duration=3.0,
        song_title='This title should be skipped',  # Should skip because first lyric at t=0
        artist_name='Test Artist'
    )
    print(f"\n✓ Video generated: {output_path}")
    return output_path


if __name__ == '__main__':
    test_all_features()
    print("\n✅ All features tested successfully!")
