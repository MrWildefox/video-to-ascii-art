# Quick Start Guide 🚀

Get started with Video to ASCII Art in 2 minutes!

## Step 1: Install Dependencies

```bash
# Clone the repository
git clone https://github.com/MrWildefox/video-to-ascii-art.git
cd video-to-ascii-art

# Install Python packages
pip install -r requirements.txt
```

**Audio Support** (Optional but recommended):

```bash
# Install ffmpeg for audio extraction
# macOS
brew install ffmpeg

# Linux
sudo apt install ffmpeg

# Windows
# Download from: https://ffmpeg.org/download.html
```

## Step 2: Convert Your First Video

### Basic playback (no audio)

```bash
python main.py -f path/to/your/video.mp4
```

### With audio and color

```bash
python main.py -f video.mp4 --audio --color
```

### More Examples

```bash
# Default 120 characters width
python main.py -f movie.mp4

# Narrower output (faster processing)
python main.py -f video.mp4 -w 80

# Simple charset (faster)
python main.py -f video.mp4 -c simple

# Play at 2x speed
python main.py -f video.mp4 --speed 2.0

# With audio and color
python main.py -f video.mp4 -w 100 --audio --color

# 2x speed with audio sync
python main.py -f video.mp4 --speed 2.0 --audio
```

## Common Commands

```bash
# Play from webcam
python main.py -f 0 -w 80

# Export frames to files
python main.py -f video.mp4 --export output_frames/

# Export with color codes
python main.py -f video.mp4 --export output_frames/ --export-color

# Download from YouTube and convert
yt-dlp -f best https://youtube.com/watch?v=... -o video.mp4
python main.py -f video.mp4 --audio --color

# Batch convert multiple videos
python examples/batch_convert.py --input videos/ --output frames/
```

## Audio & Color Features

### Audio Playback

Audio is automatically extracted and synchronized with video:

```bash
python main.py -f video.mp4 --audio
```

**Requirements:**
- `ffmpeg` installed
- `pydub` Python package (included in requirements.txt)
- Video file with audio track

**How it works:**
- Audio is extracted from video using ffmpeg
- Played in a background thread
- Automatically synchronized with frame display
- Audio time shown during playback

### Color Output

Colorize ASCII art based on video frame colors:

```bash
python main.py -f video.mp4 --color
```

**Features:**
- Automatic color mapping from video frames
- Uses 24-bit truecolor (requires compatible terminal)
- Falls back to 256-color or 16-color on older terminals
- Can be combined with audio for full multimedia experience

**Terminal Compatibility:**
- Modern terminals support truecolor
- macOS Terminal, iTerm2 ✓
- Windows Terminal ✓
- Linux GNOME Terminal, Konsole ✓
- Command Prompt (cmd.exe) ✗ (use Windows Terminal)

### Combined Features

Best experience - audio + color + good settings:

```bash
python main.py -f video.mp4 -w 120 --audio --color
```

## Performance Tips

| Goal | Command |
|------|----------|
| **Fastest** | `python main.py -f video.mp4 -w 60 -c binary --skip 2 --audio` |
| **Balanced** | `python main.py -f video.mp4 -w 100 -c standard --audio` |
| **Best Quality** | `python main.py -f video.mp4 -w 150 -c detailed --audio --color` |
| **High CPU Warning** | `python main.py -f video.mp4 -w 200 -c detailed --audio --color` |

## Character Sets

Choose different character sets:

```bash
python main.py -f video.mp4 -c standard   # Full detail (default)
python main.py -f video.mp4 -c simple     # Few characters, fast
python main.py -f video.mp4 -c detailed   # Maximum detail
python main.py -f video.mp4 -c block      # Unicode blocks
python main.py -f video.mp4 -c minimal    # Minimal characters
python main.py -f video.mp4 -c binary     # Just 2 characters
```

## Troubleshooting

### Audio Issues

**"pydub not installed" or no audio**
```bash
pip install pydub
```

**"ffmpeg not found"**
```bash
# macOS
brew install ffmpeg

# Linux
sudo apt install ffmpeg

# Windows
# Download from https://ffmpeg.org/download.html
# Or: choco install ffmpeg (if using Chocolatey)
```

**Audio out of sync**
- Audio and video should auto-sync
- If out of sync, try:
  ```bash
  python main.py -f video.mp4 --audio --skip 1
  ```
- Or disable audio:
  ```bash
  python main.py -f video.mp4
  ```

### Color Issues

**"Characters look wrong" with --color**
```bash
# Try without color
python main.py -f video.mp4

# Or try different charset
python main.py -f video.mp4 -c block --color
```

**Terminal doesn't support colors**
```bash
# Use Windows Terminal instead of Command Prompt
# Or update your terminal to latest version
```

### Video Issues

**"Video file not found"**
```bash
# Use full path
python main.py -f /full/path/to/video.mp4

# Or relative path from project directory
python main.py -f ./videos/movie.mp4
```

**"Cannot open video" (codec not supported)**
```bash
# Convert video first
ffmpeg -i input.avi -c:v libx264 output.mp4
python main.py -f output.mp4 --audio --color
```

**"Slow playback" or "High CPU usage"**
```bash
# Reduce quality:
python main.py -f video.mp4 -w 60 -c simple

# Disable color (uses CPU):
python main.py -f video.mp4 --audio

# Skip frames:
python main.py -f video.mp4 --skip 2 --audio
```

## All Options

```bash
python main.py --help
```

Full output:
```
usage: main.py [-h] -f VIDEO_FILE [-w WIDTH] 
               [-c {standard,simple,detailed,block,minimal,binary}]
               [--audio] [--color] [--speed SPEED] [--skip SKIP] 
               [--export EXPORT] [--export-color]

Convert videos to ASCII art with optional audio synchronization

options:
  -h, --help            Show this help message and exit
  -f, --file VIDEO_FILE Path to video file (or camera index like "0")
  -w, --width WIDTH     Output width in characters (default: 120)
  -c, --charset {standard,simple,detailed,block,minimal,binary}
                        Character set to use (default: standard)
  --audio               Enable audio playback with synchronization
  --color               Enable color output based on video colors
  --speed SPEED         Playback speed multiplier (default: 1.0)
  --skip SKIP           Skip frames (0 = process all frames)
  --export EXPORT       Export frames to directory instead of playing
  --export-color        Include ANSI color codes when exporting
```

## Example: Download and Play YouTube Video with Audio

```bash
# Install yt-dlp if you haven't
pip install yt-dlp

# Download video (low resolution for faster processing)
yt-dlp -f 'best[height<=360]' -o video.mp4 'https://youtube.com/watch?v=YOUR_VIDEO_ID'

# Convert to ASCII art with audio and color
python main.py -f video.mp4 -w 100 --audio --color
```

## Next Steps

- See [README.md](README.md) for detailed documentation
- Check [ARCHITECTURE.md](docs/ARCHITECTURE.md) to understand how it works
- Visit [CONTRIBUTING.md](docs/CONTRIBUTING.md) to contribute
- See [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) for common issues

## System Requirements

- Python 3.8+
- Modern terminal with ANSI support
- ~500 MB for dependencies
- FFmpeg (optional, required for audio)
- Video file or webcam

## Have Fun! 🎉

Try different videos and settings to find what works best for you.

Share your creations with us on GitHub!
