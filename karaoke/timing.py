"""
Timing module for managing word timings.
"""

class WordTiming:
    """Manages timing information for words in karaoke lyrics."""
    
    def __init__(self, text, start_time, end_time):
        """
        Initialize word timing.
        
        Args:
            text: The word text
            start_time: Start time in seconds
            end_time: End time in seconds
        """
        self.text = text
        self.start_time = start_time
        self.end_time = end_time
        self.duration = end_time - start_time
    
    def get_progress(self, current_time):
        """
        Calculate progress percentage for the word at current time.
        
        Args:
            current_time: Current playback time in seconds
        
        Returns:
            Progress percentage (0-100)
        """
        if current_time < self.start_time:
            return 0.0
        elif current_time >= self.end_time:
            return 100.0
        else:
            if self.duration == 0:
                return 100.0
            progress = ((current_time - self.start_time) / self.duration) * 100
            # Round to nearest 0.2% like in React code
            progress = round(progress * 5) / 5
            return max(0.0, min(100.0, progress))
    
    def get_status(self, current_time):
        """
        Get word status at current time.
        
        Args:
            current_time: Current playback time in seconds
        
        Returns:
            Status string: 'inactive', 'active', or 'passed'
        """
        if current_time < self.start_time:
            return 'inactive'
        elif current_time >= self.start_time and current_time <= self.end_time:
            return 'active'
        else:
            return 'passed'


def create_word_timings(text, start_time, end_time):
    """
    Create word timings by splitting text into words and distributing time.
    
    Args:
        text: Full text to split into words
        start_time: Start time for the entire text
        end_time: End time for the entire text
    
    Returns:
        List of WordTiming objects
    """
    import re
    
    # Split text preserving spaces
    words = re.split(r'(\s+)', text)
    
    # Filter out empty strings
    words = [w for w in words if w]
    
    if not words:
        return []
    
    # Calculate time per word (excluding space words for time distribution)
    non_space_words = [w for w in words if not w.isspace()]
    total_duration = end_time - start_time
    
    if len(non_space_words) == 0:
        return []
    
    time_per_word = total_duration / len(non_space_words)
    
    # Create timing for each word
    timings = []
    current_time = start_time
    
    for word in words:
        if word.isspace():
            # Spaces get minimal duration
            word_end = current_time + 0.01
        else:
            word_end = current_time + time_per_word
        
        timings.append(WordTiming(word, current_time, word_end))
        current_time = word_end
    
    return timings
