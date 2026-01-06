# Video to ASCII Art 🎨

Convert any video file into mesmerizing ASCII art animations that play directly in your terminal! This Python project transforms video frames into text-based characters, creating a retro and visually stunning effect.

**NEW**: Now with synchronized audio playback and color support! 🎵🎨

## Features ✨

- 🎬 **Video to ASCII Conversion**: Convert any video format (MP4, AVI, MOV, etc.) into ASCII art
- 🔊 **Synchronized Audio**: Extract and play audio from video with perfect sync
- 🎨 **Color Support**: Colorize ASCII art based on video frame colors (truecolor/256-color)
- ⚡ **Real-time Playback**: Watch your videos play in the terminal at the correct frame rate
- 🎭 **Customizable Output**: Adjust ASCII character sets, output width, and color options
- 📁 **Multi-Format Support**: Works with all video formats supported by OpenCV and FFmpeg
- 🖥️ **Terminal-Optimized**: Designed for modern terminal emulators
- 🖱️ **Easy to Use**: Simple command-line interface with sensible defaults
- 📊 **Progress Tracking**: Shows progress bar during conversion and playback
- 🎥 **Webcam Support**: Use your camera as input source

## Prerequisites 📋

- Python 3.8 or higher
- A terminal with support for ANSI colors (optional but recommended)
- FFmpeg (required for audio support)

## Installation 🚀

### 1. Clone the Repository

```bash
git clone https://github.com/MrWildefox/video-to-ascii-art.git
cd video-to-ascii-art
```

### 2. Create a Virtual Environment (Optional but Recommended)

```bash
python -m venv venv

# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

Or install packages manually:

```bash
pip install opencv-python numpy pillow colorama tqdm pydub
```

### 4. Install FFmpeg (For Audio Support)

**macOS**:
```bash
brew install ffmpeg
```

**Ubuntu/Debian**:
```bash
sudo apt install ffmpeg
```

**Windows**:
Download from [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html) or use:
```bash
choco install ffmpeg
```

## Quick Start ⚡

The simplest way to get started:

```bash
# Basic: Play a video as ASCII art
python main.py -f path/to/video.mp4

# With audio: Play with sound
python main.py -f video.mp4 --audio

# With color: Colorized ASCII output
python main.py -f video.mp4 --color

# Full experience: Audio + Color + Good quality
python main.py -f video.mp4 -w 120 --audio --color
```

See [QUICKSTART.md](QUICKSTART.md) for more examples.

## Usage 📖

### Basic Usage

Convert and play a video:

```bash
python main.py -f path/to/video.mp4
```

### Advanced Options

```bash
python main.py -f path/to/video.mp4 -w 100 -c standard --audio --color --speed 1.0
```

#### Command-line Arguments:

- `-f, --file` **[REQUIRED]**: Path to the video file or camera index (0 for default webcam)
- `-w, --width` **[OPTIONAL]**: Output width in characters (default: 120)
- `-c, --charset` **[OPTIONAL]**: Character set to use (default: "standard")
  - `standard`: Full ASCII range with good balance
  - `simple`: Minimal set for fast processing
  - `detailed`: Extended range for maximum detail
  - `block`: Unicode block characters
  - `minimal`: Very few characters
  - `binary`: Just 2 characters
- `--audio` **[OPTIONAL]**: Enable audio playback with synchronization
- `--color` **[OPTIONAL]**: Enable color output (requires compatible terminal)
- `--speed` **[OPTIONAL]**: Playback speed multiplier (default: 1.0)
- `--skip` **[OPTIONAL]**: Skip frames (useful for faster processing)
- `--export` **[OPTIONAL]**: Export frames to directory instead of playing
- `--export-color` **[OPTIONAL]**: Include ANSI color codes when exporting

### Examples

**Play a video with 80 character width:**

```bash
python main.py -f movie.mp4 -w 80
```

**Convert with audio and colored output:**

```bash
python main.py -f video.mp4 -w 100 --audio --color
```

**Play at 2x speed:**

```bash
python main.py -f video.mp4 --speed 2.0 --audio
```

**Save frames to files:**

```bash
python main.py -f video.mp4 --export output_frames/
```

**Use webcam:**

```bash
python main.py -f 0 -w 80 --audio
```

## Audio & Color Features 🎵🎨

### Audio Playback

Extract and play audio synchronized with video:

```bash
python main.py -f video.mp4 --audio
```

**Features:**
- Automatic audio extraction using FFmpeg
- Background thread playback
- Perfect frame/audio synchronization
- Speed control affects both audio and video
- Works with most audio codecs

**Requirements:**
- FFmpeg installed
- PyDub (included in requirements.txt)
- Video file with audio track

For detailed audio documentation, see [AUDIO_AND_COLOR.md](docs/AUDIO_AND_COLOR.md).

### Color Output

Colorize ASCII based on video frame colors:

```bash
python main.py -f video.mp4 --color
```

**Features:**
- Automatic color extraction from video frames
- Support for 24-bit truecolor (16 million colors)
- Fallback to 256-color and 16-color modes
- Terminal auto-detection for best color depth

**Terminal Compatibility:**
- ✅ Windows Terminal
- ✅ macOS Terminal / iTerm2
- ✅ Linux GNOME Terminal / Konsole
- ✅ VS Code Terminal
- ❌ Command Prompt (cmd.exe) - use Windows Terminal instead

For detailed color documentation, see [AUDIO_AND_COLOR.md](docs/AUDIO_AND_COLOR.md).

## Project Structure 📁

```
video-to-ascii-art/
├── main.py                 # Entry point - CLI and playback logic
├── ascii_converter.py      # Core conversion algorithm
├── video_processor.py      # Video reading and frame extraction
├── audio_processor.py      # Audio extraction and playback
├── color_processor.py      # Color mapping and ANSI codes
├── ascii_charsets.py       # Character set definitions
├── config.py               # Configuration constants
├── requirements.txt        # Python dependencies
├── README.md               # This file
├── QUICKSTART.md           # Quick start guide
├── docs/
│   ├── ARCHITECTURE.md     # Technical design
│   ├── AUDIO_AND_COLOR.md  # Audio & color features
│   ├── CONTRIBUTING.md     # Contribution guidelines
│   └── TROUBLESHOOTING.md  # Common issues
├── examples/
│   ├── quick_start.sh      # Usage examples
│   ├── download_and_convert.sh  # YouTube download helper
│   └── batch_convert.py    # Batch processing tool
└── tests/                  # Unit tests
```

## How It Works 🔍

### The ASCII Conversion Process:

1. **Read Video Frame**: OpenCV captures each frame from the video
2. **Resize Frame**: Scale the frame to match terminal dimensions and aspect ratio
3. **Convert to Grayscale**: Transform the frame to grayscale to get brightness values
4. **Map to ASCII**: Each pixel's brightness is mapped to an ASCII character
5. **Apply Color** (Optional): Map video colors to terminal ANSI codes
6. **Display**: Print the ASCII art to the terminal
7. **Synchronize**: Audio playback synchronized with frame display
8. **Repeat**: Move to the next frame

### Audio Synchronization:

1. Audio stream extracted from video using FFmpeg
2. PyDub loads audio into memory
3. Audio plays in background thread
4. Frame display timing locked to audio playback
5. Automatic compensation for processing delays

### Why ASCII Characters?

Different ASCII characters have different "visual weights":
- Space and periods represent dark areas
- Complex symbols like `@`, `#`, `$` represent bright areas
- Middle characters represent mid-tones

This creates a visual representation of the video using only text!

## Configuration ⚙️

Edit `config.py` to customize default behavior:

```python
# Default settings
DEFAULT_WIDTH = 120
DEFAULT_HEIGHT = 40
DEFAULT_CHARSET = "standard"
ENABLE_COLOR = False
DEFAULT_SPEED = 1.0
```

## Performance Tips 🚀

### For Different Systems:

**High-end (Modern CPU/GPU):**
```bash
python main.py -f video.mp4 -w 150 --audio --color
```

**Mid-range:**
```bash
python main.py -f video.mp4 -w 100 --audio --color
```

**Low-end:**
```bash
python main.py -f video.mp4 -w 80 --audio
```

### Optimization Strategies:

- **Larger Videos**: Use smaller width (`-w 80`) for faster processing
- **Smoother Playback**: Reduce color processing (skip `--color`)
- **Better Quality**: Increase width and use `detailed` charset
- **Fastest Speed**: Use `binary` charset with small width and skip frames

## Performance Benchmarks 📊

| Resolution | Width | FPS | Terminal | Audio |
|-----------|-------|-----|----------|-------|
| 1920x1080 | 120   | 15  | macOS Terminal | Yes |
| 1280x720  | 100   | 20  | Windows Terminal | Yes |
| 640x480   | 80    | 30  | Linux GNOME | Yes |

*Actual performance depends on your system specifications and terminal emulator*

## Troubleshooting 🐛

See [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) for solutions to common issues:

- Audio issues (extraction, playback, sync)
- Color/terminal issues
- Video loading issues
- Performance problems
- Platform-specific issues

## Advanced Features 🎯

### Batch Processing

Convert multiple videos:

```bash
python examples/batch_convert.py --input videos/ --output frames/
```

### YouTube Download & Convert

Download and convert YouTube videos:

```bash
bash examples/download_and_convert.sh "https://youtube.com/watch?v=..."
```

Requires: `yt-dlp`

### Custom Character Sets

Edit `ascii_charsets.py` to add your own:

```python
MY_CHARSET = "█▓▒░ "
```

## Contributing 🤝

We welcome contributions! Please read [CONTRIBUTING.md](docs/CONTRIBUTING.md) for:
- Code of conduct
- How to report bugs
- How to suggest features
- How to submit pull requests
- Style guide

## License 📄

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments 🙏

- Based on ASCII art conversion principles
- Inspired by retro computer aesthetics
- Built with OpenCV, NumPy, PyDub, and Python community libraries
- Thanks to all contributors and users!

## Resources 📚

- [OpenCV Documentation](https://docs.opencv.org/)
- [PyDub Documentation](https://github.com/jiaaro/pydub)
- [FFmpeg Documentation](https://ffmpeg.org/documentation.html)
- [ASCII Art on Wikipedia](https://en.wikipedia.org/wiki/ASCII_art)
- [Terminal ANSI Color Codes](https://en.wikipedia.org/wiki/ANSI_escape_code)
- [Character Visual Weight](https://paulbourke.net/dataformats/asciiart/)

## Support 💬

Found a bug? Have a suggestion? Please open an issue on [GitHub Issues](https://github.com/MrWildefox/video-to-ascii-art/issues).

---

**Happy ASCII Converting! 🎨✨**

Try different videos and settings to find what works best for you.
Share your creations with us on GitHub!
