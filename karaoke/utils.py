"""
Utility functions for karaoke effect.
"""

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
