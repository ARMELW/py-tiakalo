"""
Renderer module for drawing karaoke frames.
"""

from PIL import Image, ImageDraw
import numpy as np
from .utils import map_in_range


class KaraokeRenderer:
    """Renders karaoke effect frame by frame."""
    
    def __init__(self, width=1280, height=720, bg_color=(0, 0, 0, 255)):
        """
        Initialize karaoke renderer.
        
        Args:
            width: Frame width in pixels
            height: Frame height in pixels
            bg_color: Background color as RGBA tuple
        """
        self.width = width
        self.height = height
        self.bg_color = bg_color
    
    def render_frame(self, word_timings, word_sizes, text_layout, current_time,
                     active_color=(255, 69, 0, 255), inactive_color=(136, 136, 136, 255),
                     y_position=None):
        """
        Render a single frame at the given time.
        
        Args:
            word_timings: List of WordTiming objects
            word_sizes: List of word size dictionaries from TextLayout
            text_layout: TextLayout object for font information
            current_time: Current time in seconds
            active_color: Color for active/passed words (R, G, B, A)
            inactive_color: Color for inactive words (R, G, B, A)
            y_position: Y position for text (None = center)
        
        Returns:
            NumPy array representing the frame (H x W x 3 in BGR format for OpenCV)
        """
        # Create PIL image
        img = Image.new('RGBA', (self.width, self.height), self.bg_color)
        
        # Calculate total width and height
        total_width = sum(w['width'] for w in word_sizes)
        max_height = max(w['height'] for w in word_sizes) if word_sizes else 0
        
        # Calculate starting position (center text horizontally)
        start_x = (self.width - total_width) / 2
        if y_position is None:
            y_position = (self.height - max_height) / 2
        
        # Calculate progress width for fill effect
        total_progress_time = 0
        for timing in word_timings:
            status = timing.get_status(current_time)
            if status == 'passed':
                total_progress_time += 1
            elif status == 'active':
                progress = timing.get_progress(current_time)
                total_progress_time += progress / 100
        
        # Draw each word
        for i, (timing, word_info) in enumerate(zip(word_timings, word_sizes)):
            word_text = word_info['text']
            word_width = word_info['width']
            word_x = start_x + word_info['widthRange'][0]
            
            # Apply uppercase style if needed
            from .utils import parse_text_style
            styles = parse_text_style(text_layout.style)
            if styles.get('uppercase'):
                word_text = word_text.upper()
            
            status = timing.get_status(current_time)
            
            if status == 'inactive':
                # Draw inactive word in gray
                self._draw_text(img, word_text, word_x, y_position, 
                              text_layout.font, inactive_color)
            
            elif status == 'passed':
                # Draw passed word in active color
                self._draw_text(img, word_text, word_x, y_position,
                              text_layout.font, active_color)
            
            elif status == 'active':
                # Draw active word with progressive fill
                progress = timing.get_progress(current_time)
                
                # Draw base (inactive) word
                self._draw_text(img, word_text, word_x, y_position,
                              text_layout.font, inactive_color)
                
                # Calculate fill width
                fill_width = map_in_range(progress, 0, 100, 0, word_width, constrain=True)
                
                # Create a mask for the filled portion
                if fill_width > 0:
                    # Create a temporary image for the active text
                    temp_img = Image.new('RGBA', (self.width, self.height), (0, 0, 0, 0))
                    self._draw_text(temp_img, word_text, word_x, y_position,
                                  text_layout.font, active_color)
                    
                    # Create a mask that reveals only the filled portion
                    mask = Image.new('L', (self.width, self.height), 0)
                    mask_draw = ImageDraw.Draw(mask)
                    mask_draw.rectangle(
                        [word_x, 0, word_x + fill_width, self.height],
                        fill=255
                    )
                    
                    # Composite the active text onto the main image using the mask
                    img = Image.composite(temp_img, img, mask)
        
        # Convert PIL image to OpenCV format (BGR)
        img_rgb = img.convert('RGB')
        img_array = np.array(img_rgb)
        # Convert RGB to BGR for OpenCV
        img_bgr = img_array[:, :, ::-1]
        
        return img_bgr
    
    def _draw_text(self, img, text, x, y, font, color):
        """
        Draw text on image.
        
        Args:
            img: PIL Image object
            text: Text to draw
            x: X position
            y: Y position
            font: PIL Font object
            color: RGBA color tuple
        """
        draw = ImageDraw.Draw(img)
        draw.text((x, y), text, font=font, fill=color)
