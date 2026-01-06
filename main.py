#!/usr/bin/env python3
"""
Video to ASCII Art Converter with Audio Support
Main entry point for the application.

Usage:
    python main.py -f video.mp4 -w 120
    python main.py -f video.mp4 -w 100 --audio --color
    python main.py -f video.mp4 -w 100 --speed 1.5 --audio
"""

import argparse
import sys
import time
import os
from pathlib import Path
from typing import Optional

try:
    import cv2
    import numpy as np
except ImportError:
    print("Error: Required packages not installed.")
    print("Install with: pip install -r requirements.txt")
    sys.exit(1)

from ascii_converter import ASCIIConverter
from video_processor import VideoProcessor
from audio_processor import AudioProcessor, AudioSynchronizer
from color_processor import ColorProcessor
from ascii_charsets import list_charsets
from config import (
    DEFAULT_WIDTH, ENABLE_COLOR, DEFAULT_SPEED,
    SHOW_PROGRESS, DEFAULT_CHARSET
)


class ASCIIVideoPlayer:
    """
    Main video player that converts and displays video as ASCII art with optional audio.
    """
    
    def __init__(self, video_path: str, width: int = DEFAULT_WIDTH,
                 charset: str = DEFAULT_CHARSET, color: bool = ENABLE_COLOR,
                 speed: float = DEFAULT_SPEED, skip: int = 0, audio: bool = False):
        """
        Initialize the ASCII video player.
        
        Args:
            video_path: Path to video file
            width: Output width in characters
            charset: Character set to use
            color: Enable color output
            speed: Playback speed multiplier
            skip: Skip frames
            audio: Enable audio playback
        """
        self.video_path = video_path
        self.width = width
        self.charset = charset
        self.color = color
        self.speed = speed
        self.skip = skip
        self.audio_enabled = audio
        
        try:
            self.processor = VideoProcessor(video_path)
            self.converter = ASCIIConverter(width, charset)
            self.color_processor = ColorProcessor(use_truecolor=True) if color else None
            
            # Initialize audio if enabled
            self.audio_processor = None
            if audio:
                self.audio_processor = AudioProcessor(video_path)
                self.audio_processor.extract_audio()
            
            self.synchronizer = AudioSynchronizer(
                self.processor.fps, 
                self.audio_processor
            )
            
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
    
    def print_frame(self, frame_ascii: str) -> None:
        """
        Print a frame to the terminal.
        
        Args:
            frame_ascii: ASCII representation of the frame
        """
        # Clear terminal
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # Print frame
        print(frame_ascii)
    
    def play(self) -> None:
        """
        Play the video as ASCII art with optional audio.
        """
        print(f"\n=== ASCII Video Player with Audio ===")
        print(f"Video: {self.video_path}")
        print(f"Dimensions: {self.processor.width}x{self.processor.height}")
        print(f"FPS: {self.processor.fps:.2f}")
        print(f"Total Frames: {self.processor.frame_count}")
        print(f"Output Width: {self.width} characters")
        print(f"Charset: {self.charset}")
        print(f"Color: {'Enabled' if self.color else 'Disabled'}")
        print(f"Audio: {'Enabled' if self.audio_enabled else 'Disabled'}")
        print(f"Speed: {self.speed}x")
        print(f"\nStarting playback... Press Ctrl+C to stop.\n")
        time.sleep(2)
        
        # Start synchronization and audio
        self.synchronizer.start(play_audio=self.audio_enabled)
        
        try:
            frame_num = 0
            frame_count = 0
            total_frames = self.processor.frame_count
            
            for frame_idx, frame in self.processor.get_frames(skip=self.skip):
                start_time = time.time()
                
                # Convert frame to ASCII
                if self.color and self.color_processor:
                    # Get ASCII array for colorization
                    ascii_array = self.converter.get_ascii_array(frame)
                    frame_ascii = self.color_processor.colorize_frame(frame, ascii_array)
                else:
                    frame_ascii = self.converter.frame_to_ascii(frame)
                
                # Print frame
                self.print_frame(frame_ascii)
                
                # Show playback info
                audio_time = ""
                if self.audio_processor and self.audio_processor.is_playing:
                    audio_time = f" | Audio: {self.synchronizer.get_audio_duration():.1f}s"
                
                if SHOW_PROGRESS and total_frames > 0:
                    progress = (frame_count / total_frames) * 100
                    print(f"\n[{'='*30}] {progress:.1f}% - Frame {frame_count}/{total_frames}{audio_time}", 
                          end='', flush=True)
                else:
                    print(f"\nFrame: {frame_count}{audio_time}", end='', flush=True)
                
                # Synchronize with audio (if playing) or maintain frame rate
                processing_time = time.time() - start_time
                self.synchronizer.wait_for_frame(
                    speed_multiplier=self.speed,
                    processing_time=processing_time
                )
                
                frame_count += 1
            
            # Playback finished
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"\n=== Playback Complete ===")
            print(f"Total frames played: {frame_count}")
            print(f"Average FPS: {frame_count / (self.processor.fps / self.speed) if self.processor.fps > 0 else 0:.2f}")
            print("\nPress any key to exit...")
            
        except KeyboardInterrupt:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("\n\nPlayback interrupted by user.")
            print(f"Frames played: {frame_count}")
        
        finally:
            self.processor.close()
            if self.audio_processor:
                self.audio_processor.cleanup()
    
    def export_frames(self, output_dir: str = "output_frames/", include_color: bool = False) -> None:
        """
        Export all frames as text files.
        
        Args:
            output_dir: Directory to save frames
            include_color: Include ANSI color codes in output
        """
        Path(output_dir).mkdir(exist_ok=True)
        
        print(f"Exporting frames to {output_dir}...")
        
        for frame_num, frame in self.processor.get_frames(skip=self.skip):
            # Convert frame to ASCII
            if include_color and self.color_processor:
                ascii_array = self.converter.get_ascii_array(frame)
                frame_ascii = self.color_processor.colorize_frame(frame, ascii_array)
            else:
                frame_ascii = self.converter.frame_to_ascii(frame)
            
            # Save frame
            filename = f"{output_dir}frame_{frame_num:06d}.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(frame_ascii)
            
            if SHOW_PROGRESS and frame_num % 10 == 0:
                print(f"Exported {frame_num} frames...", end='\r')
        
        print(f"\nExport complete! {frame_num + 1} frames saved.")
        self.processor.close()


def main():
    """
    Main entry point.
    """
    parser = argparse.ArgumentParser(
        description="Convert videos to ASCII art with optional audio synchronization",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s -f video.mp4
  %(prog)s -f video.mp4 -w 100 --audio --color
  %(prog)s -f video.mp4 -w 80 -c simple --speed 2.0 --audio
  %(prog)s -f 0 -w 80  # Webcam input
        """
    )
    
    parser.add_argument('-f', '--file', dest='video_file', required=True,
                        help='Path to video file (or camera index like "0")')
    
    parser.add_argument('-w', '--width', dest='width', type=int, default=DEFAULT_WIDTH,
                        help=f'Output width in characters (default: {DEFAULT_WIDTH})')
    
    parser.add_argument('-c', '--charset', dest='charset', default=DEFAULT_CHARSET,
                        choices=list_charsets(),
                        help=f'Character set to use (default: {DEFAULT_CHARSET})')
    
    parser.add_argument('--audio', dest='audio', action='store_true',
                        help='Enable audio playback (requires ffmpeg and pydub)')
    
    parser.add_argument('--color', dest='color', action='store_true',
                        help='Enable color output')
    
    parser.add_argument('--speed', dest='speed', type=float, default=DEFAULT_SPEED,
                        help=f'Playback speed multiplier (default: {DEFAULT_SPEED})')
    
    parser.add_argument('--skip', dest='skip', type=int, default=0,
                        help='Skip frames (0 = process all frames)')
    
    parser.add_argument('--export', dest='export', type=str, default=None,
                        help='Export frames to directory instead of playing')
    
    parser.add_argument('--export-color', dest='export_color', action='store_true',
                        help='Include ANSI color codes when exporting frames')
    
    args = parser.parse_args()
    
    # Validate arguments
    if args.width < 20:
        print("Error: Width must be at least 20 characters", file=sys.stderr)
        sys.exit(1)
    
    if args.width > 300:
        print("Warning: Very large widths may be slow", file=sys.stderr)
    
    if args.speed <= 0:
        print("Error: Speed must be positive", file=sys.stderr)
        sys.exit(1)
    
    # Check for audio dependencies if requested
    if args.audio:
        try:
            from pydub import AudioSegment
        except ImportError:
            print("Error: pydub not installed. Required for audio playback.")
            print("Install with: pip install pydub")
            sys.exit(1)
        
        try:
            import subprocess
            subprocess.run(['ffmpeg', '-version'], capture_output=True, timeout=5)
        except (FileNotFoundError, subprocess.TimeoutExpired):
            print("Warning: ffmpeg not found. Audio extraction will not work.")
            print("Install ffmpeg:")
            print("  macOS: brew install ffmpeg")
            print("  Linux: sudo apt install ffmpeg")
            print("  Windows: https://ffmpeg.org/download.html")
            args.audio = False
    
    # Create and run player
    player = ASCIIVideoPlayer(
        video_path=args.video_file,
        width=args.width,
        charset=args.charset,
        color=args.color,
        speed=args.speed,
        skip=args.skip,
        audio=args.audio
    )
    
    if args.export:
        player.export_frames(args.export, include_color=args.export_color)
    else:
        player.play()


if __name__ == '__main__':
    main()
