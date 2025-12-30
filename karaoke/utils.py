"""
Utility functions for karaoke effect.
"""

import subprocess
import os


# Constants
DEFAULT_OVERLAY_OPACITY = 128  # 50% opacity (0-255 scale)
MIN_TITLE_THRESHOLD = 2.0  # Minimum seconds needed to show title


def add_audio_to_video(video_path, audio_path, output_path, audio_offset=0.0):
    """
    Add audio track to video using ffmpeg.
    
    Args:
        video_path: Path to input video file (without audio)
        audio_path: Path to audio file to add
        output_path: Path to output video file (with audio)
        audio_offset: Offset in seconds to delay/advance audio (positive = delay, negative = advance)
    
    Returns:
        Path to output video file
        
    Raises:
        RuntimeError: If ffmpeg command fails
        FileNotFoundError: If input files don't exist
        ValueError: If audio_offset is not a valid number
    """
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video file not found: {video_path}")
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")
    
    # Validate audio_offset to prevent command injection
    try:
        audio_offset = float(audio_offset)
    except (ValueError, TypeError):
        raise ValueError(f"Invalid audio_offset: must be a number, got {audio_offset}")
    
    # Build ffmpeg command
    # -y: overwrite output file
    # -i: input files
    # -itsoffset: offset audio (must come BEFORE the audio input it affects)
    # -c:v copy: copy video codec without re-encoding
    # -c:a aac: encode audio as AAC
    # -shortest: finish when shortest stream ends
    cmd = [
        'ffmpeg',
        '-y',  # Overwrite output
        '-i', video_path,  # Video input
    ]
    
    # Add audio offset if specified - MUST come before audio input
    if audio_offset != 0:
        cmd.extend(['-itsoffset', str(audio_offset), '-i', audio_path])
    else:
        cmd.extend(['-i', audio_path])
    
    cmd.extend([
        '-c:v', 'copy',  # Copy video stream
        '-c:a', 'aac',  # Encode audio as AAC
        '-shortest',  # End when shortest stream ends
        output_path
    ])
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )
        return output_path
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"ffmpeg failed: {e.stderr}")


def map_in_range(value, in_min, in_max, out_min, out_max, constrain=False):
    """
    Map a value from one range to another.
    
    Args:
        value: Input value to map
        in_min: Minimum of input range
        in_max: Maximum of input range
        out_min: Minimum of output range
        out_max: Maximum of output range
        constrain: If True, constrain output to [out_min, out_max]
    
    Returns:
        Mapped value
    """
    out_value = (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
    
    if not constrain:
        return out_value
    
    if out_value > out_max:
        return out_max
    
    if out_value < out_min:
        return out_min
    
    return out_value


def parse_text_style(styles):
    """
    Parse text style string into style attributes.
    
    Args:
        styles: Space-separated style string (e.g., 'bold italic underline')
    
    Returns:
        Dictionary with style attributes
    """
    if not styles:
        return {}
    
    style_array = styles.split(' ')
    style_object = {}
    
    if 'bold' in style_array:
        style_object['bold'] = True
    if 'italic' in style_array:
        style_object['italic'] = True
    if 'underline' in style_array:
        style_object['underline'] = True
    if 'uppercase' in style_array:
        style_object['uppercase'] = True
    
    return style_object
