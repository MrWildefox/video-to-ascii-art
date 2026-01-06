#!/usr/bin/env python3
"""
Audio processing and playback with synchronization.
Handles extracting audio from video and playing it synchronized with ASCII frames.
"""

import os
import subprocess
import threading
import time
import tempfile
from pathlib import Path
from typing import Optional
import sys

try:
    from pydub import AudioSegment
except ImportError:
    AudioSegment = None


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
        self.audio_file_path = None
        self.is_playing = False
        self.play_thread = None
        self.playback_process = None
        self.playback_start_time = None
        self.audio_duration = 0
        self._temp_audio_file = None
        
    def extract_audio(self, output_format: str = "wav") -> Optional[AudioSegment]:
        """
        Extract audio from video file using ffmpeg and save to temp file.
        
        Args:
            output_format: Audio format (wav, mp3, etc.)
            
        Returns:
            AudioSegment object or None if extraction fails
        """
        # Check if ffmpeg is available
        try:
            result = subprocess.run(['ffmpeg', '-version'], 
                                  capture_output=True, timeout=5, 
                                  creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0)
            if result.returncode != 0:
                print("Warning: ffmpeg not found. Cannot extract audio.")
                return None
        except (FileNotFoundError, subprocess.TimeoutExpired):
            print("Warning: ffmpeg not available. Cannot extract audio.")
            print("Install ffmpeg:")
            print("  macOS: brew install ffmpeg")
            print("  Linux: sudo apt install ffmpeg")
            print("  Windows: choco install ffmpeg")
            return None
        
        try:
            print(f"Extracting audio from {self.video_path}...")
            
            # Create temporary file for audio
            self._temp_audio_file = tempfile.NamedTemporaryFile(
                suffix=f'.{output_format}', delete=False
            )
            self.audio_file_path = self._temp_audio_file.name
            self._temp_audio_file.close()
            
            # Extract audio using ffmpeg directly
            cmd = [
                'ffmpeg',
                '-i', self.video_path,
                '-vn',  # No video
                '-acodec', 'pcm_s16le' if output_format == 'wav' else 'libmp3lame',
                '-ar', '44100',  # Sample rate
                '-ac', '2',  # Stereo
                '-y',  # Overwrite
                self.audio_file_path
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                timeout=60,
                creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
            )
            
            if result.returncode != 0:
                print(f"Warning: Could not extract audio: {result.stderr.decode()}")
                return None
            
            # Get duration using ffprobe
            try:
                cmd_probe = [
                    'ffprobe',
                    '-v', 'error',
                    '-show_entries', 'format=duration',
                    '-of', 'default=noprint_wrappers=1:nokey=1',
                    self.audio_file_path
                ]
                result = subprocess.run(
                    cmd_probe,
                    capture_output=True,
                    timeout=10,
                    creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
                )
                self.audio_duration = float(result.stdout.decode().strip())
            except:
                self.audio_duration = 0
            
            print(f"Audio extracted: {self.audio_duration:.2f} seconds")
            
            # Load with pydub if available for metadata
            if AudioSegment:
                try:
                    self.audio_data = AudioSegment.from_file(self.audio_file_path)
                except:
                    pass
            
            return self.audio_data
            
        except Exception as e:
            print(f"Warning: Could not extract audio: {e}")
            return None
    
    def get_audio_duration(self) -> float:
        """
        Get audio duration in seconds.
        
        Returns:
            Duration in seconds
        """
        return self.audio_duration
    
    def play_async(self, delay: float = 0, volume: float = 1.0) -> None:
        """
        Start playing audio asynchronously using system player.
        
        Args:
            delay: Delay before starting playback (seconds)
            volume: Volume level (0.0 to 1.0) - not implemented for all players
        """
        if not self.audio_file_path or not os.path.exists(self.audio_file_path):
            print("Warning: No audio file to play")
            return
        
        # Stop any existing playback
        self.stop()
        
        def playback_thread():
            try:
                self.is_playing = True
                self.playback_start_time = time.time()
                
                # Wait for delay if specified
                if delay > 0:
                    time.sleep(delay)
                
                # Platform-specific audio playback
                if sys.platform == 'win32':
                    # Windows: Try ffplay first, then fallback to PowerShell
                    try:
                        # Try ffplay (comes with ffmpeg)
                        self.playback_process = subprocess.Popen(
                            ['ffplay', '-nodisp', '-autoexit', '-loglevel', 'quiet', 
                             self.audio_file_path],
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL,
                            creationflags=subprocess.CREATE_NO_WINDOW
                        )
                        self.playback_process.wait()
                    except FileNotFoundError:
                        # Fallback to PowerShell Windows Media Player
                        ps_command = f'''Add-Type -AssemblyName presentationCore; 
                        $mediaPlayer = New-Object system.windows.media.mediaplayer; 
                        $mediaPlayer.open(\"{self.audio_file_path}\"); 
                        $mediaPlayer.Play(); 
                        Start-Sleep -Seconds {int(self.audio_duration) + 1}'''
                        
                        self.playback_process = subprocess.Popen(
                            ['powershell', '-Command', ps_command],
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL,
                            creationflags=subprocess.CREATE_NO_WINDOW
                        )
                        self.playback_process.wait()
                
                elif sys.platform == 'darwin':
                    # macOS: Use afplay
                    self.playback_process = subprocess.Popen(
                        ['afplay', self.audio_file_path],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL
                    )
                    self.playback_process.wait()
                
                else:
                    # Linux: Try multiple players
                    players = ['ffplay', 'aplay', 'paplay', 'mpg123']
                    for player in players:
                        try:
                            cmd = [player]
                            if player == 'ffplay':
                                cmd.extend(['-nodisp', '-autoexit', '-loglevel', 'quiet'])
                            cmd.append(self.audio_file_path)
                            
                            self.playback_process = subprocess.Popen(
                                cmd,
                                stdout=subprocess.DEVNULL,
                                stderr=subprocess.DEVNULL
                            )
                            self.playback_process.wait()
                            break
                        except FileNotFoundError:
                            continue
                
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
        if self.playback_process:
            try:
                self.playback_process.terminate()
                self.playback_process.wait(timeout=1)
            except:
                try:
                    self.playback_process.kill()
                except:
                    pass
            self.playback_process = None
    
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
        return self.audio_file_path is not None and os.path.exists(self.audio_file_path)
    
    def cleanup(self) -> None:
        """
        Clean up resources.
        """
        self.stop()
        
        # Clean up temporary audio file
        if self.audio_file_path and os.path.exists(self.audio_file_path):
            try:
                os.unlink(self.audio_file_path)
            except:
                pass
        
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
