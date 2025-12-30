"""
Example demonstrating all new Karafun features.
"""

from karaoke import generate_karafun_video


def example_with_all_features():
    """Complete example with all new features enabled."""
    
    lyrics_data = [
        {
            'text': 'Welcome to the Karafun style karaoke',
            'start_time': 0,
            'end_time': 3
        },
        {
            'text': 'Watch the words turn magenta as you sing',
            'start_time': 3,
            'end_time': 6
        },
        {
            'text': 'Two lines displayed at the same time',
            'start_time': 6,
            'end_time': 9
        },
        {
            'text': 'With a beautiful header and title screen',
            'start_time': 9,
            'end_time': 12
        },
        {
            'text': 'Time remaining is displayed below',
            'start_time': 12,
            'end_time': 15
        },
        {
            'text': 'Typewriter animation on the title',
            'start_time': 15,
            'end_time': 18
        }
    ]
    
    print("Generating complete Karafun demo with all features...")
    print("\nFeatures enabled:")
    print("  ✓ Typewriter animation for title")
    print("  ✓ Progressive underline animation")
    print("  ✓ Time remaining display")
    print("  ✓ Two-line alternating display")
    print("  ✓ Header with branding")
    print("  ✓ Background color support")
    print()
    
    output_path = generate_karafun_video(
        lyrics_data=lyrics_data,
        output_path='karafun_complete_demo.mp4',
        width=1280,
        height=720,
        fps=30,
        font_size=52,
        style='bold',
        bg_color=(10, 10, 30),  # Dark blue background
        show_header=True,
        show_time=True,  # NEW: Show time display
        title_duration=4.0,
        song_title='Ny Fanahiko',  # Matches the screenshot
        artist_name='Ndriana Ramamonjy',  # Matches the screenshot
        typewriter_speed=0.05  # NEW: Typewriter animation speed
    )
    
    print(f"✓ Video generated: {output_path}")
    print(f"\nVideo features:")
    print(f"  - Resolution: 1280x720 HD")
    print(f"  - Duration: ~22 seconds (4s title + 18s lyrics)")
    print(f"  - Typewriter title animation")
    print(f"  - Progressive underline animation")
    print(f"  - Time remaining counter")
    print(f"  - Two-line karaoke display")


def example_with_config():
    """Example showing how to use the CLI with config file."""
    print("\n" + "="*70)
    print("CLI USAGE EXAMPLE")
    print("="*70)
    print("\nYou can also generate videos using a JSON config file:")
    print("\n  python -m karaoke.cli --config config_example.json")
    print("\nOr with a custom output path:")
    print("\n  python -m karaoke.cli --config config.json --output my_video.mp4")
    print("\nSee config_example.json for the configuration structure.")
    print("="*70)


if __name__ == '__main__':
    example_with_all_features()
    example_with_config()
    
    print("\n✓ Demo completed successfully!")
