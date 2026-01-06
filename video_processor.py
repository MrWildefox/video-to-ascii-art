#!/usr/bin/env python3
"""
Video processing and frame extraction.
"""

import cv2
import numpy as np
from typing import Iterator, Tuple, Optional
import os


class VideoProcessor:
    """
    Handles video file reading and frame processing.
    """
    
    def __init__(self, video_path: str):
        """
        Initialize video processor.
        
        Args:
            video_path: Path to video file or camera index
            
        Raises:
            ValueError: If video cannot be opened
        """
        # Handle camera input (integer as string)
        try:
            camera_index = int(video_path)
            self.video_path = camera_index
        except ValueError:
            if not os.path.exists(video_path):
                raise ValueError(f"Video file not found: {video_path}")
            self.video_path = video_path
        
        # Open video
        self.cap = cv2.VideoCapture(self.video_path)
        
        if not self.cap.isOpened():
            raise ValueError(f"Cannot open video: {self.video_path}")
        
        # Get video properties
        self._fps = self.cap.get(cv2.CAP_PROP_FPS) or 30
        self._frame_count = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self._width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self._height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self._is_camera = isinstance(self.video_path, int)
        
    @property
    def fps(self) -> float:
        """Get frames per second."""
        return self._fps
    
    @property
    def frame_count(self) -> int:
        """Get total number of frames."""
        return self._frame_count
    
    @property
    def width(self) -> int:
        """Get frame width."""
        return self._width
    
    @property
    def height(self) -> int:
        """Get frame height."""
        return self._height
    
    @property
    def is_camera(self) -> bool:
        """Check if source is camera."""
        return self._is_camera
    
    def get_frame(self, frame_num: Optional[int] = None) -> Optional[np.ndarray]:
        """
        Get a specific frame or the next frame.
        
        Args:
            frame_num: Frame number to get (None = get next frame)
            
        Returns:
            Frame as numpy array or None if end of video
        """
        if frame_num is not None:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
        
        ret, frame = self.cap.read()
        if not ret:
            return None
        return frame
    
    def get_frames(self, skip: int = 0) -> Iterator[Tuple[int, np.ndarray]]:
        """
        Iterate through all frames in the video.
        
        Args:
            skip: Number of frames to skip (0 = process all)
            
        Yields:
            Tuple of (frame_number, frame_data)
        """
        frame_num = 0
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break
            
            if skip > 0 and frame_num % (skip + 1) != 0:
                frame_num += 1
                continue
            
            yield frame_num, frame
            frame_num += 1
    
    def reset(self) -> None:
        """
        Reset video to the beginning.
        """
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    
    def close(self) -> None:
        """
        Close the video file.
        """
        if self.cap:
            self.cap.release()
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
    
    def __del__(self):
        """Cleanup on deletion."""
        self.close()
