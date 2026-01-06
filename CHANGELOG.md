# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2026-01-06

### Added

#### Audio Support 🎵
- **Audio extraction** from video files using FFmpeg
- **Audio playback** with PyDub in background thread
- **Audio synchronization** - frames synchronized with audio playback
- `--audio` flag to enable audio playback
- `AudioProcessor` class for audio handling
- `AudioSynchronizer` class for frame/audio timing
- Support for all FFmpeg-compatible audio formats (MP3, WAV, OGG, AAC, FLAC, etc.)
- Automatic audio duration calculation
- Speed control affects both video and audio playback

#### Color Support 🎨
- **Color mapping** from video frames to terminal colors
- **Truecolor support** (24-bit RGB) for modern terminals
- **256-color fallback** for older terminals
- **16-color fallback** for basic terminal support
- `--color` flag to enable color output
- `ColorProcessor` class with multiple color depth modes
- Automatic color detection based on terminal capabilities
- Color support for frame export (`--export-color`)

#### Documentation
- New file: `docs/AUDIO_AND_COLOR.md` - Comprehensive guide for audio and color features
- Updated `README.md` with audio/color information
- Updated `QUICKSTART.md` with audio/color examples
- New `CHANGELOG.md` file

#### Dependencies
- Added `pydub` (0.25.1) for audio processing
- Updated `requirements.txt` with all new dependencies

#### CLI Enhancements
- `--audio` flag for audio playback
- `--color` flag for color output
- `--export-color` flag to include colors when exporting frames
- Improved help text in `--help` output
- Better error messages for missing dependencies

### Changed

- Updated `main.py` to integrate audio and color support
- Enhanced `ASCIIVideoPlayer` class with audio/color features
- Improved `VideoProcessor` with synchronization support
- Updated `ascii_converter.py` with `get_ascii_array()` method for colorization
- `requirements.txt` now includes pydub

### Technical Details

#### Audio Implementation
- Audio extracted once at startup
- Playback in daemon thread (doesn't block video playback)
- Synchronization based on playback time, not system clock
- Automatic delay compensation for frame processing
- Graceful fallback to system timing if audio unavailable

#### Color Implementation
- RGB to 256-color conversion using 6x6x6 color cube
- ANSI escape codes for terminal color support
- Per-character colorization
- Minimal CPU overhead (~20-30%)
- Automatic terminal capability detection

### Performance Impact

- Audio playback: +0% (separate thread, minimal overhead)
- Color output: +20-30% CPU usage
- Combined (audio + color): +20-30% CPU usage

### Breaking Changes

None. All changes are backward compatible.

### Deprecations

None.

## [1.0.0] - Initial Release

### Added

- Core video to ASCII conversion
- Multiple character sets (standard, simple, detailed, block, minimal, binary)
- Real-time playback in terminal
- Customizable output width
- Customizable playback speed
- Frame skipping for performance
- Webcam support
- Frame export to text files
- Command-line interface
- Comprehensive documentation
- GitHub Actions CI/CD workflows
- Unit tests
- Example scripts for batch processing

### Features

- Video format support: All OpenCV-compatible formats
- Character sets: 6 built-in options
- Terminal support: ANSI-capable terminals
- Platform support: Windows, macOS, Linux

---

## Installation Notes

### For Version 2.0.0

Audio support requires FFmpeg:

```bash
# macOS
brew install ffmpeg

# Linux
sudo apt install ffmpeg

# Windows
choco install ffmpeg
# Or download from https://ffmpeg.org/download.html
```

Color support requires a modern terminal emulator:
- Windows Terminal (not Command Prompt)
- macOS Terminal or iTerm2
- Linux GNOME Terminal or Konsole

### Updating from 1.0.0 to 2.0.0

```bash
git pull origin main
pip install -r requirements.txt
ffmpeg --version  # Verify FFmpeg installation
```

No code changes needed - existing commands work as before.
New flags (`--audio`, `--color`) are optional.

---

## Known Issues

### Audio
- Audio sync may drift slightly on very slow systems
- Some video codecs may not have audio tracks
- FFmpeg must be installed for audio support

### Color
- Windows Command Prompt doesn't support ANSI colors (use Windows Terminal)
- Very old terminals may not support colors properly
- Color processing adds ~20-30% CPU overhead

### General
- Very large video dimensions (>400 width) may be slow
- Terminal performance varies significantly between emulators
- On Windows, Unicode characters may not display in Command Prompt

---

## Future Roadmap

### Planned for v2.1.0
- [ ] Volume control during playback
- [ ] Audio visualization
- [ ] Subtitle support
- [ ] HTML5 export

### Planned for v3.0.0
- [ ] GPU acceleration (CUDA/OpenCL)
- [ ] Streaming support (HTTP/RTMP)
- [ ] Effect filters (edge detection, blur, etc.)
- [ ] Multi-threaded processing

### Under Consideration
- Beat-sync visual effects
- Real-time webcam effects
- Network streaming
- Web player integration
- Mobile app version

---

## Contributing

See [CONTRIBUTING.md](docs/CONTRIBUTING.md) for how to contribute.

## License

MIT License - see [LICENSE](LICENSE) for details.
