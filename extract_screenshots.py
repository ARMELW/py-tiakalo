"""
Extract frames from test videos to show visual changes.
"""

import cv2
import os


def extract_frame(video_path, time_seconds, output_path):
    """Extract a frame from video at specified time."""
    if not os.path.exists(video_path):
        print(f"Video not found: {video_path}")
        return False
    
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_number = int(time_seconds * fps)
    
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
    ret, frame = cap.read()
    
    cap.release()
    
    if ret:
        cv2.imwrite(output_path, frame)
        print(f"✓ Extracted frame: {output_path}")
        return True
    else:
        print(f"Failed to extract frame from {video_path}")
        return False


if __name__ == '__main__':
    print("Extracting frames to demonstrate changes...\n")
    
    # Extract frame showing transparent header
    extract_frame('comprehensive_test.mp4', 4.0, 'screenshot_transparent_header.png')
    
    # Extract frame showing "Remaining:" time during pause
    extract_frame('comprehensive_test.mp4', 10.0, 'screenshot_remaining_time.png')
    
    # Extract frame showing simple time format during singing
    extract_frame('comprehensive_test.mp4', 4.5, 'screenshot_simple_time.png')
    
    # Extract frame showing overlay on background
    extract_frame('test_bg_overlay.mp4', 3.0, 'screenshot_overlay.png')
    
    print("\n✅ All screenshots extracted!")
