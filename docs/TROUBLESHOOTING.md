# Troubleshooting Guide

## Common Issues and Solutions

### Installation Issues

#### "No module named 'cv2'"

**Problem**: OpenCV not installed

**Solution**:
```bash
pip install opencv-python
```

Or reinstall all dependencies:
```bash
pip install -r requirements.txt
```

#### "No module named 'numpy'"

**Problem**: NumPy not installed

**Solution**:
```bash
pip install numpy
```

#### Python version incompatibility

**Problem**: Script fails with version error

**Solution**:
```bash
python --version  # Should be 3.8 or higher
python3 main.py -f video.mp4  # Use python3 explicitly
```

### Video Input Issues

#### "Video file not found"

**Problem**: Cannot locate video file

**Solutions**:
1. Check file path is correct
2. Use absolute path: `/full/path/to/video.mp4`
3. Ensure file extension is lowercase (`.mp4` not `.MP4`)
4. Check file permissions

```bash
# Using absolute path
python main.py -f /Users/username/videos/movie.mp4

# Or relative path from project directory
python main.py -f ./videos/movie.mp4
```

#### "Cannot open video"

**Problem**: Video format not supported

**Solutions**:
1. Install ffmpeg (required for many codecs):
   - **macOS**: `brew install ffmpeg`
   - **Ubuntu**: `sudo apt install ffmpeg`
   - **Windows**: Download from https://ffmpeg.org/download.html

2. Convert video to supported format:
   ```bash
   ffmpeg -i input.avi -c:v libx264 output.mp4
   ```

3. Try different video file

#### Webcam not working

**Problem**: Can't use camera with `-f 0`

**Solutions**:
1. Check camera permissions
2. Try different camera index: `-f 1` or `-f 2`
3. Close other applications using camera
4. On Linux, ensure user is in video group:
   ```bash
   sudo usermod -a -G video $USER
   ```

### Terminal Display Issues

#### ASCII frames not clearing properly

**Problem**: Previous frames visible in terminal

**Solutions**:
1. Use terminal that supports ANSI escape codes:
   - Windows: Windows Terminal (not cmd.exe)
   - macOS: Terminal or iTerm2
   - Linux: Most terminals (xterm, GNOME Terminal, etc.)

2. Test ANSI support:
   ```bash
   echo -e "\033[2J\033[H"  # Should clear screen
   ```

3. Try with smaller width:
   ```bash
   python main.py -f video.mp4 -w 80
   ```

#### Characters appear garbled or incorrect

**Problem**: Terminal encoding issues

**Solutions**:
1. Ensure UTF-8 encoding:
   - Windows: Use Windows Terminal instead of cmd.exe
   - macOS/Linux: `export LANG=en_US.UTF-8`

2. Try different character set:
   ```bash
   python main.py -f video.mp4 -c simple
   ```

3. Use block characters (better compatibility):
   ```bash
   python main.py -f video.mp4 -c block
   ```

#### Playback is very slow

**Problem**: Low FPS or jerky playback

**Solutions**:
1. Reduce output width:
   ```bash
   python main.py -f video.mp4 -w 60  # Smaller = faster
   ```

2. Skip frames:
   ```bash
   python main.py -f video.mp4 --skip 2  # Process every 3rd frame
   ```

3. Use simpler character set:
   ```bash
   python main.py -f video.mp4 -c simple
   ```

4. Close other applications to free resources

5. Check system performance:
   - macOS: `top`
   - Linux: `htop` or `top`
   - Windows: Task Manager

### Performance Issues

#### High CPU usage

**Problem**: CPU maxed out during playback

**Solutions**:
1. Reduce output dimensions
2. Skip more frames
3. Close background applications
4. Consider GPU-accelerated version (future)

#### Out of memory error

**Problem**: "MemoryError" or system freezes

**Solutions**:
1. Reduce output width significantly
2. Skip more frames
3. Close other applications
4. Consider processing shorter video segment

#### Video plays at wrong speed

**Problem**: Video too fast or too slow

**Solutions**:
1. Adjust speed multiplier:
   ```bash
   python main.py -f video.mp4 --speed 0.5  # Slower
   python main.py -f video.mp4 --speed 2.0  # Faster
   ```

2. Check CPU load (slow playback often due to lag)

### Character Set Issues

#### "Unknown charset"

**Problem**: Invalid charset name

**Solution**: Use one of the valid charsets:
```bash
python main.py -f video.mp4 -c standard  # valid
python main.py -f video.mp4 -c mycharset  # invalid
```

Available: `standard`, `simple`, `detailed`, `block`, `minimal`, `binary`

#### Output doesn't look right

**Problem**: ASCII quality not good

**Solutions**:
1. Try different charset:
   ```bash
   python main.py -f video.mp4 -c detailed  # More detail
   ```

2. Increase output width:
   ```bash
   python main.py -f video.mp4 -w 150
   ```

3. Try block characters:
   ```bash
   python main.py -f video.mp4 -c block
   ```

## Platform-Specific Issues

### Windows

**Issue**: "Command not found" or script won't run

**Solutions**:
```bash
# Use python directly
python main.py -f video.mp4

# Or python3
python3 main.py -f video.mp4

# Use full path if installed to different location
C:\Python310\python.exe main.py -f video.mp4
```

**Issue**: Characters look wrong in Command Prompt

**Solution**: Use Windows Terminal instead of Command Prompt

### macOS

**Issue**: "Permission denied" when running script

**Solution**:
```bash
chmod +x main.py
python main.py -f video.mp4
```

**Issue**: Can't find ffmpeg

**Solution**:
```bash
brew install ffmpeg
```

### Linux

**Issue**: Black screen or no video output

**Solution**: Ensure graphics/display works:
```bash
# Test with simple display
echo "Test" | less
```

**Issue**: Camera permission denied

**Solution**:
```bash
sudo usermod -a -G video $USER
# Then log out and back in
```

## Advanced Troubleshooting

### Debug mode

Add verbose output:

```python
# In config.py, set:
VERBOSE = True
```

### Test video compatibility

```bash
# Test if OpenCV can read video
python -c "
import cv2
cap = cv2.VideoCapture('video.mp4')
print(f'FPS: {cap.get(cv2.CAP_PROP_FPS)}')
print(f'Frames: {cap.get(cv2.CAP_PROP_FRAME_COUNT)}')
cap.release()
"
```

### Check terminal capabilities

```bash
# Test ANSI support
echo -e '\033[31mRed\033[0m'  # Should print red text

# Check character encoding
echo $LANG  # Should contain UTF-8
```

## Getting Help

If issues persist:

1. Check [GitHub Issues](https://github.com/MrWildefox/video-to-ascii-art/issues)
2. Search existing issues for your problem
3. Create new issue with:
   - Error message (full stack trace)
   - Command used
   - System info (OS, Python version, terminal type)
   - Video file info (format, resolution, codec)

4. Include:
   ```bash
   python --version
   pip list | grep -E "cv|numpy|pillow"
   ```

Good luck! 🍀
