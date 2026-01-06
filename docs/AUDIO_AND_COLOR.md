# Audio & Color Features Guide

## Overview

Video to ASCII Art now supports:
- **Audio Playback**: Synchronized audio extracted from video files
- **Color Output**: ASCII art colored based on video frame colors
- **Advanced Synchronization**: Perfect timing between audio and visual display

## Audio Support

### How It Works

1. **Extraction**: FFmpeg extracts audio from the video file
2. **Loading**: PyDub loads the audio into memory
3. **Playback**: Audio plays in a background thread
4. **Synchronization**: Frame display timing is synchronized with audio playback

### Installation

#### FFmpeg (Required for Audio)

**macOS**:
```bash
brew install ffmpeg
```

**Ubuntu/Debian**:
```bash
sudo apt install ffmpeg
```

**Fedora/RHEL**:
```bash
sudo dnf install ffmpeg
```

**Windows**:
1. Download from: https://ffmpeg.org/download.html
2. Add to PATH environment variable

Or using Chocolatey:
```bash
choco install ffmpeg
```

#### Python Packages

```bash
pip install -r requirements.txt
```

This includes:
- `pydub` - Audio processing library
- `opencv-python` - Video processing
- All other dependencies

### Usage

#### Basic Audio Playback

```bash
python main.py -f video.mp4 --audio
```

This will:
1. Extract audio from the video
2. Start audio playback in background
3. Display ASCII frames synchronized with audio

#### With Other Options

```bash
# Audio with custom width
python main.py -f video.mp4 -w 80 --audio

# Audio with color
python main.py -f video.mp4 --audio --color

# Audio with 2x speed playback
python main.py -f video.mp4 --audio --speed 2.0

# Audio with frame skipping (for high performance)
python main.py -f video.mp4 --audio --skip 2
```

### Audio Synchronization

The synchronizer ensures:

1. **Frame Timing**: Frames are displayed at the correct time relative to audio
2. **Speed Control**: `--speed` multiplier affects both audio and video
3. **Processing Compensation**: Accounts for frame processing time
4. **Fallback**: If audio stops, video continues with system timing

### How Synchronization Works

```python
# Algorithm:
expected_frame_time = frame_number * (1 / fps) / speed_multiplier
actual_time = audio.current_playback_time()  # or system time
sleep_duration = expected_frame_time - actual_time - processing_time

if sleep_duration > 0:
    sleep(sleep_duration)
```

This ensures perfect synchronization between audio and visual output.

### Supported Audio Formats

PyDub supports:
- MP3
- WAV
- OGG
- AAC
- FLAC (if ffmpeg configured)
- Most common audio codecs

### Performance Notes

- Audio extraction: One-time cost at startup
- Audio playback: Minimal CPU overhead (runs in separate thread)
- Memory: Entire audio file loaded into RAM
  - Example: 1 minute of audio ≈ 1-5 MB (depends on bitrate)

### Troubleshooting

#### "ffmpeg not found"

FFmpeg is not installed or not in PATH.

```bash
# Check installation
ffmpeg -version

# Install (see Installation section above)
```

#### "pydub not installed"

Install pydub:
```bash
pip install pydub
```

#### "Can't extract audio"

Possible causes:
1. Video has no audio track
2. Audio codec not supported
3. Corrupted audio stream

Try:
```bash
# Check audio stream
ffprobe video.mp4

# Convert to MP4 with common codec
ffmpeg -i input.avi -c:a aac output.mp4
python main.py -f output.mp4 --audio
```

#### "Audio out of sync"

If audio drifts:

1. Try without color (reduces frame processing time):
   ```bash
   python main.py -f video.mp4 --audio -w 80
   ```

2. Use narrower ASCII width (faster processing):
   ```bash
   python main.py -f video.mp4 -w 60 --audio
   ```

3. Use simpler character set:
   ```bash
   python main.py -f video.mp4 -c simple --audio
   ```

## Color Support

### How It Works

1. **Pixel Mapping**: Each frame position is mapped to corresponding video pixel
2. **Color Extraction**: RGB values extracted from video frame
3. **Character Colorization**: ASCII characters colored with ANSI codes
4. **Terminal Rendering**: Terminal displays colored text

### Color Modes

Three color depth options (automatic selection):

#### 1. Truecolor (24-bit RGB)

- **Colors**: 16 million (2^24)
- **Quality**: Maximum (true colors from video)
- **Support**: Modern terminals (iTerm2, Windows Terminal, etc.)
- **Format**: `\033[38;2;R;G;Bm`

#### 2. 256-Color

- **Colors**: 256 colors
- **Quality**: Good (downsampled from full palette)
- **Support**: Most terminals
- **Format**: `\033[38;5;Nm` (N = 0-255)

#### 3. 16-Color (Fallback)

- **Colors**: 16 basic ANSI colors
- **Quality**: Low (basic colors)
- **Support**: All terminals
- **Format**: `\033[3Xm` (X = 0-7)

### Usage

#### Basic Color Output

```bash
python main.py -f video.mp4 --color
```

#### With Audio

```bash
python main.py -f video.mp4 --audio --color
```

#### Full Quality Setup

```bash
python main.py -f video.mp4 -w 120 --audio --color
```

### Terminal Compatibility

**Supported (Truecolor)**:
- ✅ macOS Terminal
- ✅ iTerm2
- ✅ Windows Terminal
- ✅ GNOME Terminal (3.16+)
- ✅ Konsole
- ✅ VS Code Terminal
- ✅ kitty

**Limited Support (256-color)**:
- ⚠️ PuTTY (with configuration)
- ⚠️ MobaXterm
- ⚠️ Older terminal emulators

**Not Supported**:
- ❌ Command Prompt (cmd.exe) - use Windows Terminal
- ❌ Very old terminals

### Performance Impact

Color processing adds overhead:

| Color Mode | CPU Cost | Typical FPS Impact |
|------------|----------|-------------------|
| No color | Baseline | No impact |
| 256-color | +20% | -3-5 FPS |
| Truecolor | +30% | -5-10 FPS |

If performance is poor:

```bash
# Disable color
python main.py -f video.mp4 -w 100

# Or use narrower width
python main.py -f video.mp4 -w 60 --color
```

### Color Mapping Algorithm

RGB to 256-color conversion:

```python
# Map RGB to 6x6x6 color cube
r_index = round(r / 255 * 5)  # 0-5
g_index = round(g / 255 * 5)  # 0-5
b_index = round(b / 255 * 5)  # 0-5

# Convert to color code
color_code = 16 + 36*r + 6*g + b
```

This provides good color approximation with minimal computation.

### Exporting with Colors

Save colored frames to text files:

```bash
python main.py -f video.mp4 --export frames/ --export-color
```

Frames will include ANSI color codes:

```bash
cat frames/frame_000000.txt  # Will display in color
```

You can view colored output:

```bash
# In terminal
less -R frames/frame_000000.txt

# Convert to HTML (optional)
# Colors preserved in terminal view
```

## Combined Audio & Color

### Best Experience

For optimal multimedia experience:

```bash
python main.py -f video.mp4 -w 120 --audio --color
```

This provides:
- Full color support (Truecolor if available)
- Synchronized audio playback
- Good ASCII resolution
- Balanced performance

### Performance Tuning

**High-end System** (Modern CPU/GPU):
```bash
python main.py -f video.mp4 -w 150 --audio --color
```

**Mid-range System**:
```bash
python main.py -f video.mp4 -w 100 --audio --color
```

**Low-end System**:
```bash
python main.py -f video.mp4 -w 80 --audio
# (without color for better performance)
```

## Advanced Configuration

### Custom Color Processing

Edit `color_processor.py` to customize:

```python
class ColorProcessor:
    def __init__(self, use_256_colors=True, use_truecolor=False):
        self.use_256_colors = use_256_colors
        self.use_truecolor = use_truecolor
```

Options:
- `use_truecolor=True` - Force 24-bit RGB
- `use_256_colors=False` - Use 16 colors
- Custom color mapping functions

### Audio Volume Control

In `audio_processor.py`:

```python
audio_processor.play_async(volume=0.8)  # 80% volume
```

### Frame Rate Compensation

The synchronizer automatically compensates for:
- Varying processing times
- System load
- Terminal rendering speed

No manual adjustment needed.

## Examples

### YouTube Video with Full Features

```bash
# Download
yt-dlp -f 'best[height<=480]' -o video.mp4 'https://youtube.com/watch?v=...'

# Convert with audio and color
python main.py -f video.mp4 -w 100 --audio --color
```

### Batch Processing with Audio

```bash
for video in videos/*.mp4; do
    python main.py -f "$video" -w 80 --audio
done
```

### Exporting for Web Display

```bash
# Export with colors
python main.py -f video.mp4 --export frames/ --export-color

# View a frame
less -R frames/frame_000000.txt
```

## Future Enhancements

- [ ] Dynamic volume control during playback
- [ ] Video-to-Audio sync adjustment
- [ ] Subtitle support
- [ ] HTML5 web player export
- [ ] Stereo/surround audio visualization
- [ ] Beat-sync effects

## References

- [PyDub Documentation](https://github.com/jiaaro/pydub)
- [FFmpeg Documentation](https://ffmpeg.org/documentation.html)
- [ANSI Color Codes](https://en.wikipedia.org/wiki/ANSI_escape_code#8-bit)
- [Terminal Colors](https://chrisyeh96.github.io/2020/03/28/terminal-colors.html)
