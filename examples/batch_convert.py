#!/usr/bin/env python3
"""
Batch convert multiple videos to ASCII art frames.

Usage:
    python examples/batch_convert.py
    python examples/batch_convert.py --input videos/ --output frames/ --width 100
"""

import os
import argparse
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import ASCIIVideoPlayer


def batch_convert(input_dir: str, output_dir: str, width: int = 120, 
                  charset: str = "standard", pattern: str = "*.mp4"):
    """
    Batch convert videos in a directory.
    
    Args:
        input_dir: Directory containing video files
        output_dir: Directory to save ASCII frames
        width: Output width in characters
        charset: Character set to use
        pattern: File pattern to match (e.g., "*.mp4")
    """
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    
    if not input_path.exists():
        print(f"Error: Input directory not found: {input_dir}")
        return
    
    # Find video files
    video_files = list(input_path.glob(pattern))
    
    if not video_files:
        print(f"No video files found matching pattern: {pattern}")
        return
    
    print(f"Found {len(video_files)} video files to process")
    print()
    
    for i, video_file in enumerate(video_files, 1):
        print(f"[{i}/{len(video_files)}] Processing: {video_file.name}")
        
        # Create output directory for this video
        video_output_dir = output_path / video_file.stem
        
        try:
            player = ASCIIVideoPlayer(
                video_path=str(video_file),
                width=width,
                charset=charset
            )
            player.export_frames(str(video_output_dir))
            print(f"  ✓ Saved to: {video_output_dir}")
        except Exception as e:
            print(f"  ✗ Error: {e}")
        
        print()
    
    print("Batch conversion complete!")


def main():
    parser = argparse.ArgumentParser(
        description="Batch convert multiple videos to ASCII art frames"
    )
    
    parser.add_argument('--input', '-i', default='videos/',
                        help='Input directory containing videos')
    parser.add_argument('--output', '-o', default='ascii_frames/',
                        help='Output directory for ASCII frames')
    parser.add_argument('--width', '-w', type=int, default=120,
                        help='Output width in characters')
    parser.add_argument('--charset', '-c', default='standard',
                        help='Character set to use')
    parser.add_argument('--pattern', '-p', default='*.mp4',
                        help='File pattern to match')
    
    args = parser.parse_args()
    
    batch_convert(
        input_dir=args.input,
        output_dir=args.output,
        width=args.width,
        charset=args.charset,
        pattern=args.pattern
    )


if __name__ == '__main__':
    main()
