#!/usr/bin/env python3
"""
Color processing for ASCII output.
Handles mapping colors from video frames to terminal colors.
"""

import numpy as np
from typing import Tuple, List


class ColorProcessor:
    """
    Handles conversion of pixel colors to terminal ANSI colors.
    """
    
    # ANSI color codes (basic 16 colors)
    ANSI_COLORS = {
        'black': 30,
        'red': 31,
        'green': 32,
        'yellow': 33,
        'blue': 34,
        'magenta': 35,
        'cyan': 36,
        'white': 37,
    }
    
    def __init__(self, use_256_colors: bool = True, use_truecolor: bool = False):
        """
        Initialize color processor.
        
        Args:
            use_256_colors: Use 256-color ANSI palette
            use_truecolor: Use 24-bit RGB color (truecolor)
        """
        self.use_256_colors = use_256_colors
        self.use_truecolor = use_truecolor
    
    @staticmethod
    def rgb_to_ansi_16(r: int, g: int, b: int) -> int:
        """
        Convert RGB to nearest ANSI 16-color code.
        
        Args:
            r, g, b: RGB values (0-255)
            
        Returns:
            ANSI color code (30-37)
        """
        # Simple RGB to 16-color conversion
        brightness = (r + g + b) // 3
        
        if brightness < 50:
            color = 30  # black
        elif brightness > 200:
            color = 37  # white
        elif r > g and r > b:
            color = 31  # red
        elif g > r and g > b:
            color = 32  # green
        elif b > r and b > g:
            color = 34  # blue
        elif r > b:
            color = 33  # yellow (red + green)
        elif g > b:
            color = 32  # green
        else:
            color = 34  # blue
        
        return color
    
    @staticmethod
    def rgb_to_256_color(r: int, g: int, b: int) -> int:
        """
        Convert RGB to nearest 256-color ANSI code.
        Uses the xterm 256-color palette.
        
        Args:
            r, g, b: RGB values (0-255)
            
        Returns:
            256-color code (0-255)
        """
        # Convert to 6x6x6 color cube
        r = round(r / 255 * 5)
        g = round(g / 255 * 5)
        b = round(b / 255 * 5)
        
        # Color cube starts at index 16
        return 16 + 36 * r + 6 * g + b
    
    @staticmethod
    def rgb_to_truecolor(r: int, g: int, b: int) -> str:
        """
        Convert RGB to 24-bit truecolor ANSI escape code.
        
        Args:
            r, g, b: RGB values (0-255)
            
        Returns:
            ANSI escape code string
        """
        return f"\033[38;2;{r};{g};{b}m"
    
    def colorize_char(self, char: str, r: int, g: int, b: int) -> str:
        """
        Add color to a character.
        
        Args:
            char: Character to colorize
            r, g, b: RGB values
            
        Returns:
            Colorized character with ANSI codes
        """
        if self.use_truecolor:
            color_code = self.rgb_to_truecolor(r, g, b)
            return f"{color_code}{char}\033[0m"
        elif self.use_256_colors:
            color_code = self.rgb_to_256_color(r, g, b)
            return f"\033[38;5;{color_code}m{char}\033[0m"
        else:
            color_code = self.rgb_to_ansi_16(r, g, b)
            return f"\033[{color_code}m{char}\033[0m"
    
    def colorize_frame(self, frame: np.ndarray, ascii_array: np.ndarray) -> str:
        """
        Colorize ASCII output based on frame colors.
        
        Args:
            frame: Original BGR frame (or grayscale)
            ascii_array: ASCII character array
            
        Returns:
            Colorized ASCII string
        """
        # Handle grayscale frames
        if len(frame.shape) == 2:
            # Convert grayscale to BGR for consistent processing
            frame_bgr = np.stack([frame, frame, frame], axis=2)
        else:
            frame_bgr = frame
        
        # Resize frame to match ASCII dimensions
        try:
            import cv2
            frame_resized = cv2.resize(frame_bgr, 
                                       (ascii_array.shape[1], ascii_array.shape[0]),
                                       interpolation=cv2.INTER_LINEAR)
        except:
            # Fallback if OpenCV not available
            return self._fallback_colorize(ascii_array)
        
        # Convert BGR to RGB
        if len(frame_resized.shape) == 3:
            frame_rgb = frame_resized[:, :, ::-1]  # BGR to RGB
        else:
            frame_rgb = frame_resized
        
        # Build colorized output
        lines = []
        for y in range(ascii_array.shape[0]):
            line = ""
            for x in range(ascii_array.shape[1]):
                char = ascii_array[y, x]
                
                if len(frame_rgb.shape) == 3:
                    r, g, b = frame_rgb[y, x]
                    r, g, b = int(r), int(g), int(b)
                else:
                    r = g = b = int(frame_rgb[y, x])
                
                line += self.colorize_char(char, r, g, b)
            
            lines.append(line)
        
        return "\n".join(lines)
    
    def _fallback_colorize(self, ascii_array: np.ndarray) -> str:
        """
        Fallback colorization using grayscale values.
        
        Args:
            ascii_array: ASCII character array
            
        Returns:
            Simple colorized ASCII string
        """
        lines = []
        for row in ascii_array:
            lines.append(''.join(row))
        return '\n'.join(lines)
