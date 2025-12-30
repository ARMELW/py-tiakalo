"""
Test audio support in karaoke videos.
"""

from karaoke import generate_karafun_video


def test_audio_support():
    """Test adding audio to karaoke video."""
    lyrics_data = [
        {
            'text': 'Testing audio support',
            'start_time': 0,
            'end_time': 2.5
        },
        {
            'text': 'Audio should play with video',
            'start_time': 2.5,
            'end_time': 5
        },
        {
            'text': 'This is the final test',
            'start_time': 5,
            'end_time': 7.5
        }
    ]
    
    print("Generating karaoke video with audio...")
    output_path = generate_karafun_video(
        lyrics_data=lyrics_data,
        output_path='test_with_audio.mp4',
        width=1280,
        height=720,
        fps=30,
        font_size=52,
        style='bold',
        bg_color=(10, 10, 30),
        show_header=True,
        show_time=True,
        title_duration=2.0,
        song_title='Audio Test',
        artist_name='Test Artist',
        audio_path='test_audio.mp3',  # Add test audio
        audio_offset=0.0
    )
    print(f"✓ Video with audio generated: {output_path}")


def test_audio_with_offset():
    """Test adding audio with offset."""
    lyrics_data = [
        {
            'text': 'Audio delayed by 1 second',
            'start_time': 0,
            'end_time': 3
        },
        {
            'text': 'To sync with lyrics better',
            'start_time': 3,
            'end_time': 6
        }
    ]
    
    print("\nGenerating karaoke video with delayed audio...")
    output_path = generate_karafun_video(
        lyrics_data=lyrics_data,
        output_path='test_audio_offset.mp4',
        width=1280,
        height=720,
        fps=30,
        font_size=52,
        style='bold',
        bg_color=(10, 10, 30),
        show_header=True,
        title_duration=0,  # Skip title
        audio_path='test_audio.mp3',
        audio_offset=1.0  # Delay audio by 1 second
    )
    print(f"✓ Video with delayed audio generated: {output_path}")


if __name__ == '__main__':
    test_audio_support()
    test_audio_with_offset()
    print("\n✅ All audio tests completed!")
