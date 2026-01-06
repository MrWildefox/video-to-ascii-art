#!/usr/bin/env python3
"""
Configuration settings for Video to ASCII Art converter
"""

# Terminal output settings
DEFAULT_WIDTH = 120
DEFAULT_HEIGHT = 40
DEFAULT_CHARSET = "standard"
ENABLE_COLOR = False
DEFAULT_SPEED = 1.0

# Video processing settings
VIDEO_QUALITY_SCALE = 0.7  # Scale factor for video processing (0.0-1.0)
FRAME_SKIP = 0  # Skip frames (0 = process all frames)

# ASCII conversion settings
ASPECT_RATIO_CORRECTION = 0.55  # Correction factor for character aspect ratio
TERMINAL_ASPECT_RATIO = 0.5  # Typical terminal character aspect ratio

# Color settings
USE_TRUECOLOR = True  # Use 24-bit RGB colors if available
MAX_COLORS = 256  # Maximum colors to use

# Logging
VERBOSE = False
SHOW_PROGRESS = True

# Performance
MAX_FPS = 60  # Maximum frames per second
MIN_FRAME_DELAY = 0.016  # Minimum delay between frames in seconds

# Output settings
SAVE_FRAMES = False  # Save individual frames to files
SAVE_DIRECTORY = "output_frames/"
EXPORT_FORMAT = "txt"  # 'txt', 'html', or 'both'
