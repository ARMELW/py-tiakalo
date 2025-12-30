"""
Complete showcase of Karafun-style karaoke features.
This script demonstrates all the capabilities of the Karafun renderer.
"""

from karaoke import generate_karafun_video


def showcase_all_features():
    """
    Comprehensive showcase demonstrating all Karafun features:
    - Title screen with song info
    - Header with branding
    - Two-line display
    - White to magenta color transition
    - Progressive word fill
    """
    
    # Create realistic song lyrics
    lyrics_data = [
        {
            'text': 'Welcome to tiakalo karaoke system',
            'start_time': 0,
            'end_time': 2.5
        },
        {
            'text': 'Featuring the amazing Karafun style',
            'start_time': 2.5,
            'end_time': 5.0
        },
        {
            'text': 'Two lines displayed at the same time',
            'start_time': 5.0,
            'end_time': 7.5
        },
        {
            'text': 'Watch words turn from white to pink',
            'start_time': 7.5,
            'end_time': 10.0
        },
        {
            'text': 'As you sing along with the music',
            'start_time': 10.0,
            'end_time': 12.5
        },
        {
            'text': 'Perfect for parties and events',
            'start_time': 12.5,
            'end_time': 15.0
        },
        {
            'text': 'Professional karaoke made easy',
            'start_time': 15.0,
            'end_time': 17.5
        },
        {
            'text': 'Thank you for using tiakalo',
            'start_time': 17.5,
            'end_time': 20.0
        }
    ]
    
    print("=" * 70)
    print("KARAFUN STYLE KARAOKE - COMPLETE SHOWCASE")
    print("=" * 70)
    print()
    print("This demonstration includes:")
    print("  ✓ Title screen with song information")
    print("  ✓ Professional header with branding")
    print("  ✓ Two-line lyrics display (current + next)")
    print("  ✓ White text for unsung words")
    print("  ✓ Magenta/pink highlight for sung words")
    print("  ✓ Smooth progressive fill animation")
    print()
    print("Generating video...")
    
    output_path = generate_karafun_video(
        lyrics_data=lyrics_data,
        output_path='karafun_showcase.mp4',
        width=1280,
        height=720,
        fps=30,
        font_size=52,
        style='bold',
        bg_color=(10, 10, 30),  # Dark blue background
        show_header=True,
        title_duration=4.0,
        song_title='Karafun Style Showcase',
        artist_name='tiakalo.org'
    )
    
    print()
    print("=" * 70)
    print(f"✓ Showcase video generated: {output_path}")
    print("=" * 70)
    print()
    print("Video details:")
    print(f"  - Resolution: 1280x720 (HD)")
    print(f"  - Frame rate: 30 FPS")
    print(f"  - Duration: ~24 seconds (4s title + 20s lyrics)")
    print(f"  - Style: Karafun professional")
    print()
    print("Features demonstrated:")
    print("  1. Title Screen (0-4s):")
    print("     - Song title with glow effect")
    print("     - Artist name")
    print("     - Decorative underline")
    print()
    print("  2. Header (4-24s):")
    print("     - Site branding (tiakalo.org)")
    print("     - Status indicator (♪ KARAOKE)")
    print("     - Magenta accent line")
    print()
    print("  3. Lyrics Display (4-24s):")
    print("     - Two lines visible simultaneously")
    print("     - Upper line: currently singing")
    print("     - Lower line: next line (fading in)")
    print()
    print("  4. Color Animation:")
    print("     - White (255, 255, 255) for unsung")
    print("     - Magenta (237, 61, 234) for sung")
    print("     - Smooth progressive fill")
    print()
    print("To view the video, open: karafun_showcase.mp4")
    print("=" * 70)


if __name__ == '__main__':
    showcase_all_features()
