#!/bin/bash
# Quick start examples for Video to ASCII Art

echo "Video to ASCII Art - Quick Start Examples"
echo "=========================================="
echo ""

# Example 1: Basic usage
echo "Example 1: Basic playback with default settings"
echo "Command: python main.py -f video.mp4"
echo ""

# Example 2: Custom width
echo "Example 2: Play with smaller output width (faster)"
echo "Command: python main.py -f video.mp4 -w 80"
echo ""

# Example 3: Different character set
echo "Example 3: Simple character set (faster processing)"
echo "Command: python main.py -f video.mp4 -c simple"
echo ""

# Example 4: Speed control
echo "Example 4: Playback at 2x speed"
echo "Command: python main.py -f video.mp4 --speed 2.0"
echo ""

# Example 5: Frame skipping
echo "Example 5: Skip frames for better performance"
echo "Command: python main.py -f video.mp4 --skip 2"
echo ""

# Example 6: Export frames
echo "Example 6: Save frames to text files"
echo "Command: python main.py -f video.mp4 --export output_frames/"
echo ""

# Example 7: Webcam
echo "Example 7: Play from webcam"
echo "Command: python main.py -f 0 -w 80"
echo ""

# Example 8: Detailed character set
echo "Example 8: Maximum detail with detailed charset"
echo "Command: python main.py -f video.mp4 -c detailed -w 120"
echo ""

echo "Available character sets: standard, simple, detailed, block, minimal, binary"
echo ""
echo "For more options, run: python main.py --help"
