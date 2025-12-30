"""
Example usage of Karafun-style karaoke.
"""

from karaoke import generate_karafun_video


def example_karafun_with_title():
    """Example with Karafun style, title screen, and header."""
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
        }
    ]
    
    print("Generating Karafun-style karaoke video with title screen...")
    output_path = generate_karafun_video(
        lyrics_data=lyrics_data,
        output_path='karafun_with_title.mp4',
        width=1280,
        height=720,
        fps=30,
        font_size=52,
        style='bold',
        bg_color=(10, 10, 30),  # Dark blue background
        show_header=True,
        title_duration=3.0,
        song_title='Karafun Demo Song',
        artist_name='tiakalo.org'
    )
    print(f"Video generated: {output_path}")


def example_karafun_simple():
    """Simple Karafun example without title screen."""
    lyrics_data = [
        {
            'text': 'This is a simple karaoke line',
            'start_time': 0,
            'end_time': 2.5
        },
        {
            'text': 'Another line follows right here',
            'start_time': 2.5,
            'end_time': 5
        },
        {
            'text': 'And the final line to end',
            'start_time': 5,
            'end_time': 7.5
        }
    ]
    
    print("Generating simple Karafun-style karaoke video...")
    output_path = generate_karafun_video(
        lyrics_data=lyrics_data,
        output_path='karafun_simple.mp4',
        width=1280,
        height=720,
        fps=30,
        font_size=48,
        style='bold',
        bg_color=(0, 0, 0),  # Black background
        show_header=True,
        title_duration=0  # No title screen
    )
    print(f"Video generated: {output_path}")


def example_karafun_no_header():
    """Karafun example without header - just lyrics."""
    lyrics_data = [
        {
            'text': 'Singing in the rain',
            'start_time': 0,
            'end_time': 2
        },
        {
            'text': 'Just singing in the rain',
            'start_time': 2,
            'end_time': 4
        },
        {
            'text': 'What a glorious feeling',
            'start_time': 4,
            'end_time': 6
        },
        {
            'text': 'I am happy again',
            'start_time': 6,
            'end_time': 8
        }
    ]
    
    print("Generating Karafun-style karaoke video without header...")
    output_path = generate_karafun_video(
        lyrics_data=lyrics_data,
        output_path='karafun_no_header.mp4',
        width=1280,
        height=720,
        fps=30,
        font_size=56,
        style='bold',
        bg_color=(20, 0, 40),  # Purple background
        show_header=False,
        title_duration=2.5,
        song_title='Singing in the Rain',
        artist_name='Classic Song'
    )
    print(f"Video generated: {output_path}")


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        example_name = sys.argv[1]
        if example_name == 'with_title':
            example_karafun_with_title()
        elif example_name == 'simple':
            example_karafun_simple()
        elif example_name == 'no_header':
            example_karafun_no_header()
        else:
            print(f"Unknown example: {example_name}")
            print("Available examples: with_title, simple, no_header")
    else:
        print("Running all Karafun examples...")
        example_karafun_with_title()
        print()
        example_karafun_simple()
        print()
        example_karafun_no_header()
        print("\nAll Karafun examples completed!")
