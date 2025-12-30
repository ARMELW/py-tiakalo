"""
Text layout module for measuring word dimensions using Pillow.
"""

from PIL import Image, ImageDraw, ImageFont
import os


class TextLayout:
    """Handles text measurement and layout calculations."""
    
    def __init__(self, font_family='Arial', font_size=24, style=''):
        """
        Initialize text layout.
        
        Args:
            font_family: Font family name or path to TTF file
            font_size: Font size in pixels
            style: Style string (e.g., 'bold italic')
        """
        self.font_family = font_family
        self.font_size = font_size
        self.style = style
        self.font = self._load_font()
    
    def _load_font(self):
        """Load the font based on font_family and style."""
        from .utils import parse_text_style
        
        styles = parse_text_style(self.style)
        
        # Try to load as TTF file path first
        if os.path.exists(self.font_family):
            try:
                return ImageFont.truetype(self.font_family, self.font_size)
            except:
                pass
        
        # Try common font paths
        font_paths = [
            f'/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
            f'/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf',
            f'/System/Library/Fonts/Helvetica.ttc',
            f'C:\\Windows\\Fonts\\arial.ttf',
        ]
        
        # Add bold/italic variants if needed
        if styles.get('bold') and styles.get('italic'):
            font_paths.insert(0, '/usr/share/fonts/truetype/dejavu/DejaVuSans-BoldOblique.ttf')
            font_paths.insert(0, '/usr/share/fonts/truetype/liberation/LiberationSans-BoldItalic.ttf')
        elif styles.get('bold'):
            font_paths.insert(0, '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf')
            font_paths.insert(0, '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf')
        elif styles.get('italic'):
            font_paths.insert(0, '/usr/share/fonts/truetype/dejavu/DejaVuSans-Oblique.ttf')
            font_paths.insert(0, '/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf')
        
        for font_path in font_paths:
            if os.path.exists(font_path):
                try:
                    return ImageFont.truetype(font_path, self.font_size)
                except:
                    continue
        
        # Fallback to default font
        return ImageFont.load_default()
    
    def measure_text(self, text):
        """
        Measure text dimensions.
        
        Args:
            text: Text to measure
        
        Returns:
            Tuple of (width, height)
        """
        # Handle uppercase style
        from .utils import parse_text_style
        styles = parse_text_style(self.style)
        
        if styles.get('uppercase'):
            text = text.upper()
        
        # Create a temporary image to measure text
        img = Image.new('RGBA', (1, 1), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Get bounding box
        bbox = draw.textbbox((0, 0), text, font=self.font)
        width = bbox[2] - bbox[0]
        height = bbox[3] - bbox[1]
        
        # Handle spaces with a small width
        if text.strip() == '':
            # Space width is approximately 0.2em
            space_width = self.font_size * 0.2
            return (space_width, height)
        
        return (width, height)
    
    def measure_words(self, words):
        """
        Measure dimensions for a list of words.
        
        Args:
            words: List of word strings
        
        Returns:
            List of dictionaries with word info:
            {
                'text': word text,
                'width': word width,
                'height': word height,
                'widthRange': [start_x, end_x]
            }
        """
        word_sizes = []
        current_x = 0
        
        for word in words:
            width, height = self.measure_text(word)
            word_info = {
                'text': word,
                'width': width,
                'height': height,
                'widthRange': [current_x, current_x + width]
            }
            word_sizes.append(word_info)
            current_x += width
        
        return word_sizes
    
    def get_total_dimensions(self, word_sizes):
        """
        Get total dimensions from word measurements.
        
        Args:
            word_sizes: List of word info dictionaries
        
        Returns:
            Tuple of (total_width, max_height)
        """
        if not word_sizes:
            return (0, 0)
        
        total_width = sum(w['width'] for w in word_sizes)
        max_height = max(w['height'] for w in word_sizes)
        
        return (total_width, max_height)
