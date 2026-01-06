#!/usr/bin/env python3
"""
Core ASCII conversion logic.
Handles image to ASCII character mapping.
"""

import numpy as np
from typing import List
from ascii_charsets import get_charset
from config import ASPECT_RATIO_CORRECTION, TERMINAL_ASPECT_RATIO


class ASCIIConverter:
    """
    Converts images/frames to ASCII art.
    """
    
    def __init__(self, width: int = 120, charset: str = "standard"):
        """
        Initialize ASCII converter.
        
        Args:
            width: Output width in characters
            charset: Character set to use for conversion
        """
        self.width = width
        self.charset = get_charset(charset)
        self.charset_len = len(self.charset)
        
    def resize_frame(self, frame: np.ndarray) -> np.ndarray:
        """
        Resize frame to match ASCII output dimensions.
        
        Args:
            frame: Input frame (grayscale or RGB)
            
        Returns:
            Resized frame
        """
        try:
            import cv2
        except ImportError:
            raise ImportError("OpenCV is required. Install with: pip install opencv-python")
        
        # Convert to grayscale if needed
        if len(frame.shape) == 3:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Calculate height based on aspect ratio
        height = frame.shape[0]
        width = frame.shape[1]
        aspect_ratio = height / width
        
        # Adjust for terminal character aspect ratio
        new_height = int(self.width * aspect_ratio * ASPECT_RATIO_CORRECTION)
        
        # Resize frame
        resized = cv2.resize(frame, (self.width, new_height), interpolation=cv2.INTER_LINEAR)
        return resized
    
    def frame_to_ascii(self, frame: np.ndarray) -> str:
        """
        Convert a frame to ASCII art string.
        
        Args:
            frame: Input frame (should be grayscale, 0-255 values)
            
        Returns:
            ASCII art string
        """
        # Resize frame
        resized = self.resize_frame(frame)
        
        # Ensure frame is grayscale
        if len(resized.shape) != 2:
            import cv2
            resized = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
        
        # Normalize pixel values to 0-1 range
        normalized = resized.astype(np.float32) / 255.0
        
        # Map to charset indices
        indices = (normalized * (self.charset_len - 1)).astype(np.int32)
        
        # Convert to ASCII characters
        ascii_chars = np.array([self.charset[idx] for idx in indices.flat])
        ascii_chars = ascii_chars.reshape(resized.shape)
        
        # Build output string
        lines = []
        for row in ascii_chars:
            lines.append(''.join(row))
        
        return '\n'.join(lines)
    
    def get_ascii_array(self, frame: np.ndarray) -> np.ndarray:
        """
        Get ASCII representation as a 2D array of characters.
        
        Args:
            frame: Input frame
            
        Returns:
            2D numpy array of ASCII characters
        """
        # Resize frame
        resized = self.resize_frame(frame)
        
        # Normalize pixel values
        normalized = resized.astype(np.float32) / 255.0
        
        # Map to charset indices
        indices = (normalized * (self.charset_len - 1)).astype(np.int32)
        
        # Convert to ASCII characters
        ascii_chars = np.array([self.charset[idx] for idx in indices.flat])
        ascii_chars = ascii_chars.reshape(resized.shape)
        
        return ascii_chars
    
    def get_dimensions(self, frame: np.ndarray) -> tuple:
        """
        Get the dimensions of the ASCII output for a given frame.
        
        Args:
            frame: Input frame
            
        Returns:
            Tuple of (width, height)
        """
        resized = self.resize_frame(frame)
        return (resized.shape[1], resized.shape[0])
