"""
Karafun-style karaoke renderer with two-line display and animations.
"""

from PIL import Image, ImageDraw, ImageFont
import numpy as np
from .utils import map_in_range


class KarafunRenderer:
    """Renders Karafun-style karaoke effect with two lines displayed."""
    
    def __init__(self, width=1280, height=720, bg_color=(0, 0, 0, 255)):
        """
        Initialize Karafun renderer.
        
        Args:
            width: Frame width in pixels
            height: Frame height in pixels
            bg_color: Background color as RGBA tuple
        """
        self.width = width
        self.height = height
        self.bg_color = bg_color
        
        # Karafun color scheme
        self.inactive_color = (255, 255, 255, 255)  # White for inactive
        self.done_color = (237, 61, 234, 255)  # Magenta/pink for done words
        self.active_fill_color = (255, 255, 255, 255)  # White for active filling
    
    def render_frame(self, lines_data, text_layout, current_time, 
                     show_header=True, show_title=False,
                     song_title=None, artist_name=None):
        """
        Render a single frame with Karafun style (two lines).
        
        Args:
            lines_data: List of line dictionaries with word_timings and word_sizes
            text_layout: TextLayout object for font information
            current_time: Current time in seconds
            show_header: Whether to show the header
            show_title: Whether to show title screen
            song_title: Song title for title screen
            artist_name: Artist name for title screen
        
        Returns:
            NumPy array representing the frame (H x W x 3 in BGR format for OpenCV)
        """
        # Create PIL image with background
        img = Image.new('RGBA', (self.width, self.height), self.bg_color)
        
        if show_title and song_title:
            # Show title screen
            self._render_title_screen(img, song_title, artist_name, text_layout)
        else:
            # Show header if enabled
            if show_header:
                self._render_header(img, text_layout)
            
            # Find the current and next line
            current_line = None
            next_line = None
            
            for i, line in enumerate(lines_data):
                # Current line is the one being sung
                if line['start_time'] <= current_time <= line['end_time']:
                    current_line = line
                    # Next line is the one after current
                    if i + 1 < len(lines_data):
                        next_line = lines_data[i + 1]
                    break
            
            # If no current line, check if we're before first line or after last
            if current_line is None:
                if lines_data and current_time < lines_data[0]['start_time']:
                    # Before first line - show first two lines
                    current_line = lines_data[0]
                    if len(lines_data) > 1:
                        next_line = lines_data[1]
                elif lines_data and current_time > lines_data[-1]['end_time']:
                    # After last line - show last line
                    current_line = lines_data[-1]
            
            # Calculate positions for two lines
            # Karafun style: centered vertically around 40% from top
            center_y = int(self.height * 0.40)
            
            if current_line:
                line_height = max(w['height'] for w in current_line['word_sizes']) if current_line['word_sizes'] else 60
                line_spacing = int(line_height * 0.8)
                
                # Current line position (upper line)
                current_y = center_y - line_spacing // 2
                
                # Render current line
                self._render_line(
                    img, 
                    current_line['word_timings'],
                    current_line['word_sizes'],
                    text_layout,
                    current_time,
                    current_y,
                    is_current=True,
                    line_index=0
                )
                
                # Render next line if it exists
                if next_line:
                    next_y = center_y + line_spacing // 2 + line_height
                    
                    # Calculate opacity for next line (fade in as current line progresses)
                    line_progress = 0
                    if current_line['end_time'] > current_line['start_time']:
                        line_progress = (current_time - current_line['start_time']) / (current_line['end_time'] - current_line['start_time'])
                    
                    opacity = min(1.0, line_progress * 2)  # Fade in during first half
                    
                    self._render_line(
                        img,
                        next_line['word_timings'],
                        next_line['word_sizes'],
                        text_layout,
                        current_time,
                        next_y,
                        is_current=False,
                        line_index=1,
                        opacity=opacity
                    )
        
        # Convert PIL image to OpenCV format (BGR)
        img_rgb = img.convert('RGB')
        img_array = np.array(img_rgb)
        img_bgr = img_array[:, :, ::-1]
        
        return img_bgr
    
    def _render_line(self, img, word_timings, word_sizes, text_layout, current_time, 
                     y_position, is_current=True, line_index=0, opacity=1.0):
        """
        Render a single line of lyrics with Karafun style.
        
        Args:
            img: PIL Image to draw on
            word_timings: List of WordTiming objects
            word_sizes: List of word size dictionaries
            text_layout: TextLayout object
            current_time: Current time in seconds
            y_position: Y position for the line
            is_current: Whether this is the currently playing line
            line_index: Line index (0 for current/odd, 1 for next/even)
            opacity: Line opacity (0.0 to 1.0)
        """
        if not word_timings:
            return
        
        # Calculate total width for centering
        total_width = sum(w['width'] for w in word_sizes)
        start_x = (self.width - total_width) / 2
        
        # Apply uppercase style if needed
        from .utils import parse_text_style
        styles = parse_text_style(text_layout.style)
        
        # Draw each word
        for timing, word_info in zip(word_timings, word_sizes):
            word_text = word_info['text']
            word_width = word_info['width']
            word_x = start_x + word_info['widthRange'][0]
            
            if styles.get('uppercase'):
                word_text = word_text.upper()
            
            status = timing.get_status(current_time)
            
            # Determine color based on status and whether it's current line
            if not is_current:
                # Next line: always white with opacity
                color = tuple(int(c * opacity) for c in self.inactive_color[:3]) + (int(255 * opacity),)
                self._draw_text(img, word_text, word_x, y_position, text_layout.font, color)
            
            elif status == 'inactive':
                # Inactive: white
                color = tuple(int(c * opacity) for c in self.inactive_color[:3]) + (int(255 * opacity),)
                self._draw_text(img, word_text, word_x, y_position, text_layout.font, color)
            
            elif status == 'passed':
                # Passed: magenta/pink
                color = tuple(int(c * opacity) for c in self.done_color[:3]) + (int(255 * opacity),)
                self._draw_text(img, word_text, word_x, y_position, text_layout.font, color)
            
            elif status == 'active':
                # Active: progressive fill from white to white (the fill itself is white on white base)
                progress = timing.get_progress(current_time)
                
                # Draw base in white
                base_color = tuple(int(c * opacity) for c in self.inactive_color[:3]) + (int(255 * opacity),)
                self._draw_text(img, word_text, word_x, y_position, text_layout.font, base_color)
                
                # Calculate fill width
                fill_width = map_in_range(progress, 0, 100, 0, word_width, constrain=True)
                
                # Draw the filled portion in done color (magenta)
                if fill_width > 0:
                    temp_img = Image.new('RGBA', (self.width, self.height), (0, 0, 0, 0))
                    fill_color = tuple(int(c * opacity) for c in self.done_color[:3]) + (int(255 * opacity),)
                    self._draw_text(temp_img, word_text, word_x, y_position, text_layout.font, fill_color)
                    
                    # Create mask for filled portion
                    mask = Image.new('L', (self.width, self.height), 0)
                    mask_draw = ImageDraw.Draw(mask)
                    mask_draw.rectangle(
                        [word_x, 0, word_x + fill_width, self.height],
                        fill=int(255 * opacity)
                    )
                    
                    # Composite
                    img.paste(temp_img, (0, 0), mask)
    
    def _render_header(self, img, text_layout):
        """
        Render Karafun-style header with site name and status.
        
        Args:
            img: PIL Image to draw on
            text_layout: TextLayout object
        """
        draw = ImageDraw.Draw(img)
        
        # Header background with transparency
        header_height = 80
        header_rect = Image.new('RGBA', (self.width, header_height), (0, 0, 0, 51))  # 20% opacity
        img.paste(header_rect, (0, 0), header_rect)
        
        # Draw decorative top line
        draw.line([(0, 0), (self.width, 0)], fill=(237, 61, 234, 255), width=2)
        
        # Site name on the left
        site_name = "tiakalo.org"
        font_size = 32
        try:
            header_font = ImageFont.truetype(text_layout.font.path, font_size)
        except:
            header_font = text_layout.font
        
        draw.text((30, 25), site_name, font=header_font, fill=(255, 255, 255, 255))
        
        # Status indicator on the right
        status_text = "♪ KARAOKE"
        status_x = self.width - 200
        
        # Draw status background
        status_bg = Image.new('RGBA', (150, 40), (237, 61, 234, 77))  # 30% opacity
        img.paste(status_bg, (status_x, 20), status_bg)
        
        draw.text((status_x + 15, 25), status_text, font=header_font, fill=(255, 255, 255, 255))
    
    def _render_title_screen(self, img, title, artist, text_layout):
        """
        Render title screen with song title and artist name.
        
        Args:
            img: PIL Image to draw on
            title: Song title
            artist: Artist name
            text_layout: TextLayout object
        """
        draw = ImageDraw.Draw(img)
        
        # Create larger font for title
        title_size = int(text_layout.font_size * 1.8)
        artist_size = int(text_layout.font_size * 1.2)
        
        try:
            title_font = ImageFont.truetype(text_layout.font.path, title_size)
            artist_font = ImageFont.truetype(text_layout.font.path, artist_size)
        except:
            title_font = text_layout.font
            artist_font = text_layout.font
        
        # Measure text
        title_bbox = draw.textbbox((0, 0), title, font=title_font)
        title_width = title_bbox[2] - title_bbox[0]
        title_height = title_bbox[3] - title_bbox[1]
        
        if artist:
            artist_text = f"> {artist} <"
            artist_bbox = draw.textbbox((0, 0), artist_text, font=artist_font)
            artist_width = artist_bbox[2] - artist_bbox[0]
            artist_height = artist_bbox[3] - artist_bbox[1]
        else:
            artist_width = 0
            artist_height = 0
        
        # Calculate positions (centered)
        center_y = self.height // 2
        title_y = center_y - title_height - 40
        artist_y = center_y + 20
        
        # Draw title with glow effect
        title_x = (self.width - title_width) // 2
        
        # Glow effect (draw multiple times with offset)
        glow_color = (237, 61, 234, 100)
        for offset in [(-2, -2), (2, -2), (-2, 2), (2, 2)]:
            draw.text((title_x + offset[0], title_y + offset[1]), title, 
                     font=title_font, fill=glow_color)
        
        # Main title text
        draw.text((title_x, title_y), title, font=title_font, fill=(255, 255, 255, 255))
        
        # Draw decorative line under title
        line_y = title_y + title_height + 10
        line_start_x = (self.width - title_width) // 2
        line_end_x = line_start_x + title_width
        draw.line([(line_start_x, line_y), (line_end_x, line_y)], 
                 fill=(237, 61, 234, 255), width=3)
        
        # Draw artist name if provided
        if artist:
            artist_x = (self.width - artist_width) // 2
            draw.text((artist_x, artist_y), artist_text, 
                     font=artist_font, fill=(200, 200, 200, 255))
    
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
