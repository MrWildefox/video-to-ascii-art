# Architecture Documentation

## Project Structure

The project is organized into modular components:

```
video-to-ascii-art/
├── main.py                    # CLI entry point and main application logic
├── ascii_converter.py         # Core ASCII conversion algorithm
├── video_processor.py         # Video file handling and frame extraction
├── ascii_charsets.py          # Character set definitions
├── color_processor.py         # Color handling (future)
├── config.py                  # Global configuration constants
├── requirements.txt           # Python dependencies
└── docs/
    ├── ARCHITECTURE.md        # This file
    ├── CONTRIBUTING.md        # Contribution guidelines
    └── TROUBLESHOOTING.md     # Common issues and solutions
```

## Component Details

### main.py
**Purpose**: Entry point and application orchestration
**Key Classes**:
- `ASCIIVideoPlayer`: Main player class that coordinates video processing and display

**Key Methods**:
- `play()`: Main playback loop
- `export_frames()`: Export frames as text files
- `main()`: CLI argument parsing and initialization

### ascii_converter.py
**Purpose**: Core image-to-ASCII conversion logic
**Key Classes**:
- `ASCIIConverter`: Handles image resizing and pixel-to-character mapping

**Key Methods**:
- `resize_frame()`: Resizes frame to match ASCII dimensions
- `frame_to_ascii()`: Converts a frame to ASCII string representation
- `get_ascii_array()`: Returns ASCII as 2D array
- `get_dimensions()`: Calculates output dimensions

**Algorithm**:
1. Read input frame (BGR or grayscale)
2. Convert to grayscale if needed
3. Resize to output dimensions maintaining aspect ratio
4. Normalize pixel values to 0-1 range
5. Map normalized values to character set indices
6. Convert indices to ASCII characters
7. Assemble rows into final output string

### video_processor.py
**Purpose**: Video file handling and frame extraction
**Key Classes**:
- `VideoProcessor`: Wraps OpenCV VideoCapture with convenience methods

**Key Methods**:
- `get_frame()`: Get specific frame or next frame
- `get_frames()`: Generator for iterating through all frames
- `reset()`: Reset to beginning of video
- `close()`: Clean up resources

**Properties**:
- `fps`: Frames per second
- `frame_count`: Total number of frames
- `width`, `height`: Frame dimensions
- `is_camera`: Whether source is camera input

### ascii_charsets.py
**Purpose**: Character set definitions and management
**Available Charsets**:
- `standard`: Full ASCII range with good balance
- `simple`: Minimal set for fast processing
- `detailed`: Extended range for maximum detail
- `block`: Unicode block characters
- `minimal`: Very few characters
- `binary`: Just two characters

### config.py
**Purpose**: Global configuration and constants
**Key Settings**:
- Output dimensions (DEFAULT_WIDTH, DEFAULT_HEIGHT)
- Character set selection
- Performance tuning parameters
- Logging options

## Data Flow

```
Video File
    ↓
VideoProcessor.get_frames()
    ↓ (yields frame as numpy array)
    ↓
ASCIIConverter.frame_to_ascii()
    ├─ resize_frame() → grayscale resize
    ├─ normalize → [0-1] range
    ├─ map to charset → character indices
    └─ return ASCII string
    ↓
ASCIIVideoPlayer.print_frame()
    ├─ clear terminal
    ├─ print ASCII string
    └─ manage frame timing
    ↓
Terminal Output
```

## Key Algorithms

### ASCII Conversion

The core conversion maps pixel brightness to ASCII characters:

```
Pixel Intensity (0-255)
    ↓ normalize
Value (0.0-1.0)
    ↓ multiply by charset length
Index (0-charset_len)
    ↓ lookup
ASCII Character
```

### Aspect Ratio Correction

Terminal characters are typically wider than tall. The converter accounts for this:

```
new_height = width * aspect_ratio * ASPECT_RATIO_CORRECTION
```

This prevents stretched or squashed output.

### Frame Rate Management

Playback timing is controlled by:

```
frame_delay = (1.0 / fps) / speed_multiplier
sleep_time = max(0, frame_delay - processing_time)
```

This ensures consistent playback speed regardless of processing time.

## Performance Considerations

### Optimization Strategies

1. **Frame Skipping**: Skip frames for larger outputs
   - Reduces processing time
   - May reduce visual quality

2. **Output Width**: Smaller width = faster processing
   - Width affects both conversion and terminal rendering
   - Typical range: 60-150 characters

3. **Charset Complexity**: Simpler charsets process faster
   - "binary" (2 chars) is fastest
   - "detailed" provides most detail
   - "standard" balances quality and speed

4. **Color Processing**: Optional for performance
   - Can be enabled with `--color` flag
   - Currently not implemented

### Bottlenecks

1. **OpenCV Frame Reading**: Depends on disk/codec speed
2. **ASCII Conversion**: O(width * height) in pixel operations
3. **Terminal Rendering**: Depends on terminal implementation

Typical: Reading > Rendering > Conversion

## Future Enhancements

1. **Color Support**: Map RGB to 256 colors or true color
2. **Animated Output**: Save as animated GIF
3. **Effect Filters**: Edge detection, blur, etc.
4. **Audio Sync**: Play audio during video playback
5. **GPU Acceleration**: CUDA/OpenCL for fast conversion
6. **Streaming**: Process from network streams
7. **Multi-threading**: Separate reading, conversion, display

## Testing Strategy

### Unit Tests
- ASCIIConverter with known frames
- VideoProcessor with sample videos
- Character set validation

### Integration Tests
- Full playback with various video formats
- Different charset and width combinations
- Frame skipping and speed control

### Performance Tests
- FPS measurement with different parameters
- Memory usage monitoring
- CPU usage tracking
