"""
CLI module for karaoke video generation with config file support.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, Any
from .main import generate_karafun_video


def load_config(config_path: str) -> Dict[str, Any]:
    """
    Load configuration from JSON file.
    
    Args:
        config_path: Path to JSON configuration file
    
    Returns:
        Dictionary with configuration
    """
    config_file = Path(config_path)
    if not config_file.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    
    with open(config_file, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    return config


def validate_config(config: Dict[str, Any]) -> None:
    """
    Validate configuration structure.
    
    Args:
        config: Configuration dictionary
    
    Raises:
        ValueError: If configuration is invalid
    """
    # Check required fields
    if 'lyrics' not in config:
        raise ValueError("Configuration must include 'lyrics' field")
    
    if not isinstance(config['lyrics'], list):
        raise ValueError("'lyrics' must be a list")
    
    # Validate lyrics structure
    for i, lyric in enumerate(config['lyrics']):
        if not isinstance(lyric, dict):
            raise ValueError(f"Lyric at index {i} must be a dictionary")
        
        required_fields = ['text', 'start_time', 'end_time']
        for field in required_fields:
            if field not in lyric:
                raise ValueError(f"Lyric at index {i} missing required field: {field}")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Generate Karafun-style karaoke videos',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate video from config file
  python -m karaoke.cli --config config.json
  
  # Specify custom output path
  python -m karaoke.cli --config config.json --output my_video.mp4
        """
    )
    
    parser.add_argument(
        '--config',
        type=str,
        required=True,
        help='Path to JSON configuration file'
    )
    
    parser.add_argument(
        '--output',
        type=str,
        default=None,
        help='Output video path (overrides config)'
    )
    
    args = parser.parse_args()
    
    try:
        # Load and validate configuration
        print(f"Loading configuration from: {args.config}")
        config = load_config(args.config)
        validate_config(config)
        
        # Extract configuration values with defaults
        lyrics_data = config['lyrics']
        
        # Video settings
        video_config = config.get('video', {})
        output_path = args.output or config.get('output_path', 'karaoke_output.mp4')
        width = video_config.get('width', 1280)
        height = video_config.get('height', 720)
        fps = video_config.get('fps', 30)
        
        # Background settings
        background_config = config.get('background', {})
        bg_color_raw = background_config.get('color', [0, 0, 0])
        
        # Validate and convert bg_color
        if not isinstance(bg_color_raw, (list, tuple)) or len(bg_color_raw) != 3:
            raise ValueError("Background color must be an array of 3 RGB values (e.g., [255, 0, 0])")
        
        try:
            bg_color = tuple(int(c) for c in bg_color_raw)
            if not all(0 <= c <= 255 for c in bg_color):
                raise ValueError("RGB values must be between 0 and 255")
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid background color format: {e}")
        
        bg_image = background_config.get('image', None)
        
        # Font settings
        font_config = config.get('font', {})
        font_family = font_config.get('family', 'Arial')
        font_size = font_config.get('size', 52)
        font_style = font_config.get('style', 'bold')
        
        # Title screen settings
        title_config = config.get('title', {})
        song_title = title_config.get('song', None)
        artist_name = title_config.get('artist', None)
        title_duration = title_config.get('duration', 3.0)
        
        # Animation settings
        animation_config = config.get('animation', {})
        show_header = animation_config.get('show_header', True)
        typewriter_speed = animation_config.get('typewriter_speed', 0.05)
        
        # Display settings
        display_config = config.get('display', {})
        show_time = display_config.get('show_time', True)
        
        # Audio settings
        audio_config = config.get('audio', {})
        audio_path = audio_config.get('path', None)
        audio_offset = audio_config.get('offset', 0.0)
        
        print("Generating karaoke video...")
        print(f"  Output: {output_path}")
        print(f"  Resolution: {width}x{height}")
        print(f"  FPS: {fps}")
        print(f"  Lines: {len(lyrics_data)}")
        if audio_path:
            print(f"  Audio: {audio_path} (offset: {audio_offset}s)")
        
        # Generate video
        result_path = generate_karafun_video(
            lyrics_data=lyrics_data,
            output_path=output_path,
            width=width,
            height=height,
            fps=fps,
            font_family=font_family,
            font_size=font_size,
            style=font_style,
            bg_color=bg_color,
            show_header=show_header,
            title_duration=title_duration,
            song_title=song_title,
            artist_name=artist_name,
            bg_image=bg_image,
            show_time=show_time,
            typewriter_speed=typewriter_speed,
            audio_path=audio_path,
            audio_offset=audio_offset
        )
        
        print(f"\n✓ Video generated successfully: {result_path}")
        return 0
        
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except ValueError as e:
        print(f"Configuration error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error generating video: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
