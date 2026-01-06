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

**macOS users**: Install FFmpeg for full codec support
```bash
brew install ffmpeg
```

**Linux users**: Install FFmpeg
```bash
sudo apt install ffmpeg
```

## Step 2: Convert Your First Video

```bash
# Basic usage - play a video as ASCII art
python main.py -f path/to/your/video.mp4

# Examples:
python main.py -f movie.mp4                    # Default 120 characters width
python main.py -f video.mp4 -w 80             # Narrower output (faster)
python main.py -f video.mp4 -c simple         # Simple charset (faster)
python main.py -f video.mp4 --speed 2.0       # Play at 2x speed
```

## Common Commands

```bash
# Play from webcam
python main.py -f 0 -w 80

# Export frames to files
python main.py -f video.mp4 --export output_frames/

# Download from YouTube and convert
yt-dlp -f best https://youtube.com/watch?v=... -o video.mp4
python main.py -f video.mp4

# Batch convert multiple videos
python examples/batch_convert.py --input videos/ --output frames/
```

## Performance Tips

| Goal | Command |
|------|----------|
| **Fastest** | `python main.py -f video.mp4 -w 60 -c binary --skip 2` |
| **Balanced** | `python main.py -f video.mp4 -w 100 -c standard` |
| **Best Quality** | `python main.py -f video.mp4 -w 150 -c detailed` |

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

**"Video file not found"**
```bash
# Use full path
python main.py -f /full/path/to/video.mp4

# Or relative path
python main.py -f ./videos/movie.mp4
```

**"Cannot open video" (codec not supported)**
```bash
# Install ffmpeg
brew install ffmpeg    # macOS
sudo apt install ffmpeg  # Linux

# Or convert video first
ffmpeg -i input.avi -c:v libx264 output.mp4
python main.py -f output.mp4
```

**"Slow playback" or "High CPU usage"**
```bash
# Reduce quality:
python main.py -f video.mp4 -w 60 --skip 2 -c simple
```

**"Characters look wrong"**
```bash
# Try different charset
python main.py -f video.mp4 -c block

# Or on Windows, use Windows Terminal instead of Command Prompt
```

## All Options

```bash
python main.py --help
```

Full output:
```
usage: main.py [-h] -f VIDEO_FILE [-w WIDTH] [-c {standard,simple,detailed,block,minimal,binary}]
               [--color] [--speed SPEED] [--skip SKIP] [--export EXPORT]

Convert videos to ASCII art and play in terminal

options:
  -h, --help            Show this help message and exit
  -f, --file VIDEO_FILE Path to video file (or camera index like "0")
  -w, --width WIDTH     Output width in characters (default: 120)
  -c, --charset {standard,simple,detailed,block,minimal,binary}
                        Character set to use (default: standard)
  --color               Enable color output
  --speed SPEED         Playback speed multiplier (default: 1.0)
  --skip SKIP           Skip frames (0 = process all frames)
  --export EXPORT       Export frames to directory instead of playing
```

## Example: Download and Play YouTube Video

```bash
# Install yt-dlp if you haven't
pip install yt-dlp

# Download video (low resolution for faster processing)
yt-dlp -f 'best[height<=360]' -o video.mp4 'https://youtube.com/watch?v=YOUR_VIDEO_ID'

# Convert to ASCII art
python main.py -f video.mp4 -w 100
```

## Next Steps

- See [README.md](README.md) for detailed documentation
- Check [ARCHITECTURE.md](docs/ARCHITECTURE.md) to understand how it works
- Visit [CONTRIBUTING.md](docs/CONTRIBUTING.md) to contribute
- See [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) for common issues

## Requirements

- Python 3.8+
- Modern terminal with ANSI support
- Video file or webcam
- ~500 MB for dependencies

## Have Fun! 🎉

Try different videos and settings to find what works best for you.

Share your creations with us on GitHub!
