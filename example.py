"""
Example usage of the karaoke module.
"""

from karaoke import generate_karaoke_video, generate_karaoke_video_with_lines


def example_simple():
    """Simple example with single line."""
    lyrics_data = [
        {
            'text': 'Hello world this is karaoke',
            'start_time': 0,
            'end_time': 3
        },
        {
            'text': 'Watch the words fill in',
            'start_time': 3,
            'end_time': 6
        },
        {
            'text': 'One by one progressively',
            'start_time': 6,
            'end_time': 9
        }
    ]
    
    print("Generating simple karaoke video...")
    output_path = generate_karaoke_video(
        lyrics_data=lyrics_data,
        output_path='example_simple.mp4',
        width=1280,
        height=720,
        fps=30,
        font_size=60,
        active_color=(255, 69, 0),  # Orange-red
        inactive_color=(136, 136, 136),  # Gray
        bg_color=(0, 0, 0)  # Black
    )
    print(f"Video generated: {output_path}")


def example_styled():
    """Example with styled text."""
    lyrics_data = [
        {
            'text': 'BOLD UPPERCASE TEXT',
            'start_time': 0,
            'end_time': 3
        },
        {
            'text': 'with progressive filling',
            'start_time': 3,
            'end_time': 6
        }
    ]
    
    print("Generating styled karaoke video...")
    output_path = generate_karaoke_video(
        lyrics_data=lyrics_data,
        output_path='example_styled.mp4',
        width=1280,
        height=720,
        fps=30,
        font_size=72,
        style='bold uppercase',
        active_color=(0, 255, 0),  # Green
        inactive_color=(100, 100, 100),  # Dark gray
        bg_color=(20, 20, 40)  # Dark blue
    )
    print(f"Video generated: {output_path}")


def example_multiline():
    """Example with multiple lines displayed together."""
    lyrics_data = [
        {
            'text': 'First line of the song',
            'start_time': 0,
            'end_time': 2
        },
        {
            'text': 'Second line follows here',
            'start_time': 2,
            'end_time': 4
        },
        {
            'text': 'Third line completes it',
            'start_time': 4,
            'end_time': 6
        },
        {
            'text': 'And the final verse',
            'start_time': 6,
            'end_time': 8
        }
    ]
    
    print("Generating multiline karaoke video...")
    output_path = generate_karaoke_video_with_lines(
        lyrics_data=lyrics_data,
        output_path='example_multiline.mp4',
        width=1280,
        height=720,
        fps=30,
        font_size=48,
        active_color=(255, 215, 0),  # Gold
        inactive_color=(128, 128, 128),  # Gray
        bg_color=(0, 0, 50),  # Dark blue
        line_spacing=30
    )
    print(f"Video generated: {output_path}")


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        example_name = sys.argv[1]
        if example_name == 'simple':
            example_simple()
        elif example_name == 'styled':
            example_styled()
        elif example_name == 'multiline':
            example_multiline()
        else:
            print(f"Unknown example: {example_name}")
            print("Available examples: simple, styled, multiline")
    else:
        print("Running all examples...")
        example_simple()
        print()
        example_styled()
        print()
        example_multiline()
        print("\nAll examples completed!")
