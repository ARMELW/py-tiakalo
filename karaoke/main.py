"""
Main module for generating karaoke videos.
"""

import cv2
import numpy as np
from .renderer import KaraokeRenderer
from .karafun_renderer import KarafunRenderer
from .text_layout import TextLayout
from .timing import create_word_timings


def generate_karaoke_video(
    lyrics_data,
    output_path='karaoke_output.mp4',
    width=1280,
    height=720,
    fps=30,
    font_family='Arial',
    font_size=48,
    style='',
    active_color=(255, 69, 0),
    inactive_color=(136, 136, 136),
    bg_color=(0, 0, 0)
):
    """
    Generate a karaoke video from lyrics data.
    
    Args:
        lyrics_data: List of dictionaries with 'text', 'start_time', 'end_time'
                    Example: [
                        {'text': 'Hello world', 'start_time': 0, 'end_time': 2},
                        {'text': 'This is karaoke', 'start_time': 2, 'end_time': 4}
                    ]
        output_path: Path to output MP4 file
        width: Video width in pixels
        height: Video height in pixels
        fps: Frames per second
        font_family: Font family name or TTF file path
        font_size: Font size in pixels
        style: Text style string (e.g., 'bold italic')
        active_color: RGB color tuple for active/passed text
        inactive_color: RGB color tuple for inactive text
        bg_color: RGB color tuple for background
    
    Returns:
        Path to the generated video file
    """
    # Initialize components
    renderer = KaraokeRenderer(
        width=width,
        height=height,
        bg_color=bg_color + (255,)  # Add alpha channel
    )
    
    text_layout = TextLayout(
        font_family=font_family,
        font_size=font_size,
        style=style
    )
    
    # Convert colors to RGBA
    active_color = active_color + (255,)
    inactive_color = inactive_color + (255,)
    
    # Process all lyrics to create word timings
    all_word_timings = []
    all_word_sizes = []
    
    for lyric in lyrics_data:
        text = lyric['text']
        start_time = lyric['start_time']
        end_time = lyric['end_time']
        
        # Create word timings
        word_timings = create_word_timings(text, start_time, end_time)
        
        # Measure words
        words = [wt.text for wt in word_timings]
        word_sizes = text_layout.measure_words(words)
        
        all_word_timings.extend(word_timings)
        all_word_sizes.extend(word_sizes)
    
    # Calculate video duration
    if not all_word_timings:
        raise ValueError("No lyrics data provided")
    
    video_duration = max(wt.end_time for wt in all_word_timings)
    total_frames = int(video_duration * fps)
    
    # Initialize video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    # Generate frames
    for frame_idx in range(total_frames):
        current_time = frame_idx / fps
        
        # Render frame
        frame = renderer.render_frame(
            word_timings=all_word_timings,
            word_sizes=all_word_sizes,
            text_layout=text_layout,
            current_time=current_time,
            active_color=active_color,
            inactive_color=inactive_color
        )
        
        # Write frame
        out.write(frame)
    
    # Release video writer
    out.release()
    
    return output_path


def generate_karaoke_video_with_lines(
    lyrics_data,
    output_path='karaoke_output.mp4',
    width=1280,
    height=720,
    fps=30,
    font_family='Arial',
    font_size=48,
    style='',
    active_color=(255, 69, 0),
    inactive_color=(136, 136, 136),
    bg_color=(0, 0, 0),
    line_spacing=20
):
    """
    Generate a karaoke video with multiple lines displayed.
    
    Args:
        lyrics_data: List of dictionaries with 'text', 'start_time', 'end_time'
        output_path: Path to output MP4 file
        width: Video width in pixels
        height: Video height in pixels
        fps: Frames per second
        font_family: Font family name or TTF file path
        font_size: Font size in pixels
        style: Text style string
        active_color: RGB color tuple for active/passed text
        inactive_color: RGB color tuple for inactive text
        bg_color: RGB color tuple for background
        line_spacing: Spacing between lines in pixels
    
    Returns:
        Path to the generated video file
    """
    # Initialize components
    renderer = KaraokeRenderer(
        width=width,
        height=height,
        bg_color=bg_color + (255,)
    )
    
    text_layout = TextLayout(
        font_family=font_family,
        font_size=font_size,
        style=style
    )
    
    # Convert colors to RGBA
    active_color = active_color + (255,)
    inactive_color = inactive_color + (255,)
    
    # Process lyrics line by line
    lines_data = []
    for lyric in lyrics_data:
        text = lyric['text']
        start_time = lyric['start_time']
        end_time = lyric['end_time']
        
        word_timings = create_word_timings(text, start_time, end_time)
        words = [wt.text for wt in word_timings]
        word_sizes = text_layout.measure_words(words)
        
        lines_data.append({
            'word_timings': word_timings,
            'word_sizes': word_sizes,
            'start_time': start_time,
            'end_time': end_time
        })
    
    # Calculate video duration
    if not lines_data:
        raise ValueError("No lyrics data provided")
    
    video_duration = max(line['end_time'] for line in lines_data)
    total_frames = int(video_duration * fps)
    
    # Initialize video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    # Generate frames
    for frame_idx in range(total_frames):
        current_time = frame_idx / fps
        
        # Create frame with background
        frame = np.full((height, width, 3), bg_color, dtype=np.uint8)
        
        # Find active and nearby lines
        active_lines = []
        for line_data in lines_data:
            if line_data['start_time'] <= current_time <= line_data['end_time'] + 1:
                active_lines.append(line_data)
        
        # Calculate Y positions for lines
        if active_lines:
            from PIL import Image as PILImage
            
            total_height = sum(max(w['height'] for w in line['word_sizes']) 
                             for line in active_lines)
            total_height += line_spacing * (len(active_lines) - 1)
            
            start_y = (height - total_height) / 2
            current_y = start_y
            
            # Start with base background frame
            frame = np.full((height, width, 3), bg_color, dtype=np.uint8)
            
            # Render each line
            for idx, line_data in enumerate(active_lines):
                line_height = max(w['height'] for w in line_data['word_sizes'])
                
                # Render line frame
                line_frame = renderer.render_frame(
                    word_timings=line_data['word_timings'],
                    word_sizes=line_data['word_sizes'],
                    text_layout=text_layout,
                    current_time=current_time,
                    active_color=active_color,
                    inactive_color=inactive_color,
                    y_position=current_y
                )
                
                # For all lines, overlay non-background pixels
                # Create a mask for non-background pixels
                bg_array = np.array(bg_color, dtype=np.uint8)
                mask = np.any(line_frame != bg_array, axis=2)
                
                # Copy non-background pixels to frame
                frame[mask] = line_frame[mask]
                
                current_y += line_height + line_spacing
        
        # Write frame
        out.write(frame)
    
    # Release video writer
    out.release()
    
    return output_path


def generate_karafun_video(
    lyrics_data,
    output_path='karafun_output.mp4',
    width=1280,
    height=720,
    fps=30,
    font_family='Arial',
    font_size=48,
    style='bold',
    bg_color=(0, 0, 0),
    show_header=True,
    title_duration=3.0,
    song_title=None,
    artist_name=None,
    bg_image=None,
    show_time=False,
    typewriter_speed=0.05,
    audio_path=None,
    audio_offset=0.0
):
    """
    Generate a Karafun-style karaoke video with two-line display.
    
    Features:
    - Two lines displayed (current + next)
    - White color for inactive words
    - Magenta/pink (237, 61, 234) for passed words
    - Progressive fill for active words
    - Optional header with site name and status
    - Optional title screen at the start
    - Optional background image
    - Optional time display
    - Typewriter animation for title screen
    - Optional audio track
    
    Args:
        lyrics_data: List of dictionaries with 'text', 'start_time', 'end_time'
        output_path: Path to output MP4 file
        width: Video width in pixels
        height: Video height in pixels
        fps: Frames per second
        font_family: Font family name or TTF file path
        font_size: Font size in pixels (Karafun uses large, bold fonts)
        style: Text style string (default: 'bold')
        bg_color: RGB color tuple for background
        show_header: Whether to show header with site name and status
        title_duration: Duration of title screen in seconds (0 to disable)
        song_title: Song title for title screen
        artist_name: Artist name for title screen
        bg_image: Path to background image file (optional)
        show_time: Whether to show time remaining display
        typewriter_speed: Speed of typewriter animation (seconds per character)
        audio_path: Path to audio file to add to video (optional)
        audio_offset: Offset in seconds to delay/advance audio (default: 0.0)
    
    Returns:
        Path to the generated video file
    """
    # Initialize components
    renderer = KarafunRenderer(
        width=width,
        height=height,
        bg_color=bg_color + (255,),
        bg_image=bg_image
    )
    
    text_layout = TextLayout(
        font_family=font_family,
        font_size=font_size,
        style=style
    )
    
    # Process lyrics line by line
    lines_data = []
    for lyric in lyrics_data:
        text = lyric['text']
        start_time = lyric['start_time']
        end_time = lyric['end_time']
        
        word_timings = create_word_timings(text, start_time, end_time)
        words = [wt.text for wt in word_timings]
        word_sizes = text_layout.measure_words(words)
        
        lines_data.append({
            'word_timings': word_timings,
            'word_sizes': word_sizes,
            'start_time': start_time,
            'end_time': end_time,
            'text': text
        })
    
    # Calculate video duration
    if not lines_data:
        raise ValueError("No lyrics data provided")
    
    # Check if first lyric starts too early (before minimum title duration threshold)
    # Skip title screen if first lyric starts before we can reasonably show title
    from .utils import MIN_TITLE_THRESHOLD
    first_lyric_start = lines_data[0]['start_time']
    
    # Determine if we should skip title screen
    skip_title = (title_duration > 0 and song_title and 
                  first_lyric_start < MIN_TITLE_THRESHOLD)
    
    # Add title screen duration if enabled and not skipped
    time_offset = title_duration if (title_duration > 0 and song_title and not skip_title) else 0
    video_duration = max(line['end_time'] for line in lines_data) + time_offset
    total_frames = int(video_duration * fps)
    
    # Initialize video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    # Generate frames
    for frame_idx in range(total_frames):
        current_time = frame_idx / fps
        
        # Adjust time for title screen offset
        lyrics_time = current_time - time_offset if time_offset > 0 else current_time
        
        # Determine if we should show title screen
        show_title = time_offset > 0 and current_time < time_offset
        
        # Calculate the effective time for rendering:
        # - During title screen: use absolute current_time for typewriter animation
        # - During lyrics: use adjusted lyrics_time (starts at 0 after title ends)
        time_for_animation = current_time if show_title else lyrics_time
        
        # Render frame
        frame = renderer.render_frame(
            lines_data=lines_data,
            text_layout=text_layout,
            current_time=time_for_animation,
            show_header=show_header and not show_title,
            show_title=show_title,
            song_title=song_title,
            artist_name=artist_name,
            show_time=show_time and not show_title,
            typewriter_speed=typewriter_speed,
            video_duration=video_duration - time_offset
        )
        
        # Write frame
        out.write(frame)
    
    # Release video writer
    out.release()
    
    # Add audio if provided
    if audio_path:
        from .utils import add_audio_to_video
        import os
        from pathlib import Path
        
        # Create temporary path for video without audio using proper path manipulation
        output_file = Path(output_path)
        temp_video = output_file.with_stem(f"{output_file.stem}_temp")
        os.rename(output_path, temp_video)
        
        try:
            # Merge audio with video
            add_audio_to_video(str(temp_video), audio_path, output_path, audio_offset)
            # Remove temporary file
            os.remove(temp_video)
        except Exception as e:
            # Restore original video if audio merge fails
            if os.path.exists(temp_video):
                os.rename(temp_video, output_path)
            print(f"Warning: Could not add audio: {e}")
    
    return output_path
