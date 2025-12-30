"""
Test the dark overlay on background image.
"""

from karaoke import generate_karafun_video


def test_bg_image_with_overlay():
    """Test background image with dark overlay for text visibility."""
    lyrics_data = [
        {
            'text': 'Testing text visibility',
            'start_time': 0,
            'end_time': 3
        },
        {
            'text': 'With background image overlay',
            'start_time': 3,
            'end_time': 6
        },
        {
            'text': 'Text should be readable now',
            'start_time': 6,
            'end_time': 9
        }
    ]
    
    print("Generating video with background image and dark overlay...")
    output_path = generate_karafun_video(
        lyrics_data=lyrics_data,
        output_path='test_bg_overlay.mp4',
        width=1280,
        height=720,
        fps=30,
        font_size=52,
        style='bold',
        bg_color=(10, 10, 30),
        bg_image='bg.jpg',  # Use the background image
        show_header=True,
        show_time=True,
        title_duration=2.0,
        song_title='Test Overlay',
        artist_name='Test Artist'
    )
    print(f"Video generated: {output_path}")


if __name__ == '__main__':
    test_bg_image_with_overlay()
    print("\nBackground overlay test completed!")
