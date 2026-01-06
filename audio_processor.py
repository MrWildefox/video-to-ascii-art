#!/usr/bin/env python3
"""
Audio processing and playback with synchronization.
Handles extracting audio from video and playing it synchronized with ASCII frames.
"""

import os
import subprocess
import threading
import time
from pathlib import Path
from typing import Optional
from queue import Queue

try:
    from pydub import AudioSegment
    from pydub.playback import play
except ImportError:
    AudioSegment = None
    play = None


class AudioProcessor:
    """
    Handles audio extraction and playback.
    """
    
    def __init__(self, video_path: str):
        """
        Initialize audio processor.
        
        Args:
            video_path: Path to video file
            
        Raises:
            ValueError: If audio cannot be extracted
        """
        if not os.path.exists(video_path):
            raise ValueError(f"Video file not found: {video_path}")
        
        self.video_path = video_path
        self.audio_data = None
        self.audio_file = None
        self.is_playing = False
        self.play_thread = None
        self.playback_start_time = None
        self.audio_duration = 0
        
    def extract_audio(self, output_format: str = "mp3") -> Optional[AudioSegment]:
        """
        Extract audio from video file using ffmpeg.
        
        Args:
            output_format: Audio format (mp3, wav, aac, etc.)
            
        Returns:
            AudioSegment object or None if extraction fails
        """
        if AudioSegment is None:
            print("Warning: pydub not installed. Audio will not be available.")
            print("Install with: pip install pydub")
            return None
        
        try:
            # Check if ffmpeg is available
            result = subprocess.run(['ffmpeg', '-version'], 
                                  capture_output=True, timeout=5)
            if result.returncode != 0:
                print("Warning: ffmpeg not found. Cannot extract audio.")
                return None
        except (FileNotFoundError, subprocess.TimeoutExpired):
            print("Warning: ffmpeg not available. Cannot extract audio.")
            print("Install ffmpeg:")
            print("  macOS: brew install ffmpeg")
            print("  Linux: sudo apt install ffmpeg")
            print("  Windows: https://ffmpeg.org/download.html")
            return None
        
        try:
            # Try to load audio directly using pydub
            print(f"Extracting audio from {self.video_path}...")
            
            # Determine audio codec based on input file
            audio = AudioSegment.from_file(self.video_path)
            
            self.audio_data = audio
            self.audio_duration = len(audio) / 1000.0  # Convert ms to seconds
            
            print(f"Audio extracted: {self.audio_duration:.2f} seconds")
            return audio
            
        except Exception as e:
            print(f"Warning: Could not extract audio: {e}")
            return None
    
    def get_audio_duration(self) -> float:
        """
        Get audio duration in seconds.
        
        Returns:
            Duration in seconds
        """
        if self.audio_data is None:
            return 0
        return len(self.audio_data) / 1000.0
    
    def play_async(self, delay: float = 0, volume: float = 1.0) -> None:
        """
        Start playing audio asynchronously in a separate thread.
        
        Args:
            delay: Delay before starting playback (seconds)
            volume: Volume level (0.0 to 1.0)
        """
        if self.audio_data is None:
            return
        
        if play is None:
            print("Warning: pydub playback not available")
            return
        
        # Stop any existing playback
        self.stop()
        
        def playback_thread():
            try:
                self.is_playing = True
                self.playback_start_time = time.time() - (delay / 1000.0)
                
                # Apply volume adjustment
                audio = self.audio_data
                if volume < 1.0:
                    audio = audio + (20 * (volume - 1))  # dB adjustment
                elif volume > 1.0:
                    audio = audio + (20 * (volume - 1))
                
                # Wait for delay if specified
                if delay > 0:
                    time.sleep(delay)
                
                # Play audio
                play(audio)
                self.is_playing = False
                
            except Exception as e:
                print(f"Error during audio playback: {e}")
                self.is_playing = False
        
        # Start playback in background thread
        self.play_thread = threading.Thread(target=playback_thread, daemon=True)
        self.play_thread.start()
    
    def stop(self) -> None:
        """
        Stop audio playback.
        """
        self.is_playing = False
        if self.play_thread and self.play_thread.is_alive():
            # Note: Cannot forcefully stop pydub playback, but flag is set
            pass
    
    def get_current_playback_time(self) -> float:
        """
        Get current playback time in seconds.
        
        Returns:
            Current time in seconds
        """
        if not self.is_playing or self.playback_start_time is None:
            return 0
        
        return time.time() - self.playback_start_time
    
    def is_audio_available(self) -> bool:
        """
        Check if audio is available for playback.
        
        Returns:
            True if audio can be played
        """
        return self.audio_data is not None and play is not None
    
    def cleanup(self) -> None:
        """
        Clean up resources.
        """
        self.stop()
        self.audio_data = None


class AudioSynchronizer:
    """
    Synchronizes audio playback with frame display.
    """
    
    def __init__(self, fps: float, audio_processor: Optional[AudioProcessor] = None):
        """
        Initialize synchronizer.
        
        Args:
            fps: Video frames per second
            audio_processor: AudioProcessor instance
        """
        self.fps = fps
        self.audio_processor = audio_processor
        self.frame_duration = 1.0 / fps if fps > 0 else 0.033
        self.start_time = None
        self.frame_count = 0
        
    def start(self, play_audio: bool = True) -> None:
        """
        Start synchronization.
        
        Args:
            play_audio: Whether to start audio playback
        """
        self.start_time = time.time()
        self.frame_count = 0
        
        if play_audio and self.audio_processor:
            self.audio_processor.play_async()
    
    def wait_for_frame(self, speed_multiplier: float = 1.0, 
                      processing_time: float = 0) -> None:
        """
        Wait until it's time to display the next frame.
        Accounts for audio synchronization if available.
        
        Args:
            speed_multiplier: Playback speed (1.0 = normal)
            processing_time: Time spent processing current frame
        """
        if self.start_time is None:
            self.start_time = time.time()
        
        # Calculate expected frame time
        expected_time = self.frame_count * self.frame_duration / speed_multiplier
        
        # Get actual elapsed time
        if self.audio_processor and self.audio_processor.is_playing:
            # Use audio playback time as source of truth
            actual_time = self.audio_processor.get_current_playback_time()
        else:
            # Use system time
            actual_time = time.time() - self.start_time
        
        # Calculate sleep time
        sleep_time = expected_time - actual_time - processing_time
        
        if sleep_time > 0:
            time.sleep(sleep_time)
        
        self.frame_count += 1
    
    def get_audio_duration(self) -> float:
        """
        Get total audio duration.
        
        Returns:
            Duration in seconds
        """
        if self.audio_processor:
            return self.audio_processor.get_audio_duration()
        return 0
    
    def cleanup(self) -> None:
        """
        Clean up resources.
        """
        if self.audio_processor:
            self.audio_processor.cleanup()
