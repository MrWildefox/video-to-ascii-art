#!/bin/bash
# Download a video from YouTube and convert to ASCII art
# Requires: yt-dlp, ffmpeg

if [ $# -eq 0 ]; then
    echo "Usage: $0 <youtube_url> [options]"
    echo "Example: $0 'https://www.youtube.com/watch?v=...' -w 100"
    exit 1
fi

URL="$1"
shift
EXTRA_ARGS="$@"

echo "Downloading video from YouTube..."
echo "URL: $URL"
echo ""

# Check if yt-dlp is installed
if ! command -v yt-dlp &> /dev/null; then
    echo "Error: yt-dlp not found. Install with: pip install yt-dlp"
    exit 1
fi

# Download video
VIDEO_FILE="youtube_video.mp4"
yt-dlp -f 'best[height<=360]' -o "$VIDEO_FILE" "$URL"

if [ $? -eq 0 ]; then
    echo ""
    echo "Download successful! Converting to ASCII art..."
    echo ""
    
    # Convert to ASCII
    python main.py -f "$VIDEO_FILE" $EXTRA_ARGS
    
    # Clean up
    echo ""
    read -p "Delete downloaded video? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm "$VIDEO_FILE"
        echo "Video deleted."
    fi
else
    echo "Failed to download video."
    exit 1
fi
