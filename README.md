# Video to ASCII Art 🎨

Convert any video file into mesmerizing ASCII art animations that play directly in your terminal! This Python project transforms video frames into text-based characters, creating a retro and visually stunning effect.

## Features ✨

- 🎬 **Video to ASCII Conversion**: Convert any video format (MP4, AVI, MOV, etc.) into ASCII art
- ⚡ **Real-time Playback**: Watch your videos play in the terminal at the correct frame rate
- 🎨 **Customizable Output**: Adjust ASCII character sets, output width, and color options
- 📹 **Multi-Format Support**: Works with all video formats supported by OpenCV
- 🖥️ **Terminal-Optimized**: Designed for modern terminal emulators
- 🔧 **Easy to Use**: Simple command-line interface with sensible defaults
- 📊 **Progress Tracking**: Shows progress bar during conversion

## Prerequisites 📋

- Python 3.8 or higher
- A terminal with support for ANSI colors (optional but recommended)

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
pip install opencv-python numpy pillow colorama
```

## Usage 📖

### Basic Usage

Convert and play a video:

```bash
python main.py -f path/to/video.mp4
```

### Advanced Options

```bash
python main.py -f path/to/video.mp4 -w 100 -c standard --color --speed 1.0
```

#### Command-line Arguments:

- `-f, --file` **[REQUIRED]**: Path to the video file
- `-w, --width` **[OPTIONAL]**: Output width in characters (default: 120)
- `-c, --charset` **[OPTIONAL]**: Character set to use (default: "standard")
  - `standard`: `$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^` '`
  - `simple`: `@%#*+=-:. `
  - `detailed`: Full range of ASCII characters for more detail
- `--color` **[OPTIONAL]**: Enable color output (requires capable terminal)
- `--speed` **[OPTIONAL]**: Playback speed multiplier (default: 1.0)
- `--skip` **[OPTIONAL]**: Skip every N frames (useful for larger dimensions)
- `--grayscale` **[OPTIONAL]**: Force grayscale conversion (default: auto)

### Examples

**Play a video with 80 character width:**

```bash
python main.py -f movie.mp4 -w 80
```

**Convert with colored output:**

```bash
python main.py -f video.mp4 -w 100 --color
```

**Play at 2x speed:**

```bash
python main.py -f video.mp4 --speed 2.0
```

**Save frames to files:**

```bash
python main.py -f video.mp4 --save-frames output_frames/
```

## Project Structure 📁

```
video-to-ascii-art/
├── main.py                 # Entry point - command-line interface
├── ascii_converter.py      # Core conversion logic
├── video_processor.py      # Video reading and processing
├── ascii_charsets.py       # Character set definitions
├── color_processor.py      # Color handling (optional)
├── requirements.txt        # Python dependencies
├── config.py              # Configuration constants
├── README.md              # This file
├── examples/              # Example videos and output
└── docs/                  # Additional documentation
    ├── ARCHITECTURE.md
    ├── CONTRIBUTING.md
    └── TROUBLESHOOTING.md
```

## How It Works 🔍

### The ASCII Conversion Process:

1. **Read Video Frame**: OpenCV captures each frame from the video
2. **Resize Frame**: Scale the frame to match terminal dimensions and aspect ratio
3. **Convert to Grayscale**: Transform the frame to grayscale to get brightness values
4. **Map to ASCII**: Each pixel's brightness is mapped to an ASCII character
5. **Display**: Print the ASCII art to the terminal
6. **Repeat**: Move to the next frame and repeat

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

- **Larger Videos**: Use smaller width (`-w 80`) for faster processing
- **Smoother Playback**: Reduce color processing with `--no-color`
- **Better Quality**: Increase width and use `detailed` charset
- **Real-time Play**: Ensure your terminal can handle high refresh rates

## Troubleshooting 🐛

### Terminal Clearing Issues

If the ASCII frames don't clear properly:
- Make sure your terminal supports ANSI escape codes
- Try updating your terminal emulator

### Slow Playback

- Reduce output width with `-w 60`
- Disable color mode
- Skip frames with `--skip 2`

### Video Not Found

- Check that the file path is correct
- Use absolute path: `/full/path/to/video.mp4`
- Ensure file extension is lowercase

### Character Encoding Issues

- Ensure your terminal uses UTF-8 encoding
- Some characters may not display correctly on Windows cmd

## Examples 📺

### Convert a YouTube Video

First download with yt-dlp:

```bash
pip install yt-dlp
yt-dlp "https://youtube.com/watch?v=..." -o video.mp4

# Then convert:
python main.py -f video.mp4 -w 100 --color
```

### Webcam Input

```bash
python main.py -f 0  # 0 = default webcam
```

### Process Multiple Videos

```bash
for video in videos/*.mp4; do
    python main.py -f "$video" -w 80
done
```

## Advanced Features 🔬

### Custom Character Sets

Edit `ascii_charsets.py` to add your own character sets:

```python
CUSTOM_CHARSET = "█▓▒░ "
```

### Real-time Filter Effects

Add custom filters in `video_processor.py`:

```python
def apply_edge_detection(frame):
    return cv2.Canny(frame, 100, 200)
```

### Export to File

Save ASCII frames as text or HTML:

```bash
python main.py -f video.mp4 -w 100 --export-txt frames/
```

## Performance Benchmarks 📊

| Resolution | Width | FPS | Terminal |
|-----------|-------|-----|----------|
| 1920x1080 | 120   | 15  | macOS Terminal |
| 1280x720  | 100   | 20  | Windows Terminal |
| 640x480   | 80    | 30  | Linux GNOME |

*Actual performance depends on your system specifications*

## Contributing 🤝

We welcome contributions! Please read [CONTRIBUTING.md](docs/CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License 📄

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments 🙏

- Based on principles from ASCII art conversion techniques
- Inspired by retro computer aesthetics
- Built with OpenCV and Python community libraries

## Resources 📚

- [OpenCV Documentation](https://docs.opencv.org/)
- [ASCII Art on Wikipedia](https://en.wikipedia.org/wiki/ASCII_art)
- [Terminal ANSI Color Codes](https://en.wikipedia.org/wiki/ANSI_escape_code)
- [Character Visual Weight Reference](https://paulbourke.net/dataformats/asciiart/)

## Support 💬

Found a bug? Have a suggestion? Please open an issue on [GitHub Issues](https://github.com/MrWildefox/video-to-ascii-art/issues).

---

**Happy ASCII Converting! 🎨✨**
