#!/usr/bin/env python3
"""
ASCII character sets for video-to-ascii conversion.
Each set is ordered from darkest to lightest.
"""

# Standard ASCII art charset - good balance of detail and compatibility
STANDARD_CHARSET = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. "

# Simple charset - minimal characters, quick processing
SIMPLE_CHARSET = "@%#*+=-:. "

# Detailed charset - more characters for better quality
DETAILED_CHARSET = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'.,~-+_=*%@$#"

# Block characters - uses Unicode block elements
BLOCK_CHARSET = "\u2588\u2593\u2592\u2591 "  # █ ▓ ▒ ░ (space)

# Minimal - just a few characters
MINIMAL_CHARSET = "@#*+=-:. "

# Binary - only two characters for extreme contrast
BINARY_CHARSET = "@. "

# All available charsets
CHARSETS = {
    "standard": STANDARD_CHARSET,
    "simple": SIMPLE_CHARSET,
    "detailed": DETAILED_CHARSET,
    "block": BLOCK_CHARSET,
    "minimal": MINIMAL_CHARSET,
    "binary": BINARY_CHARSET,
}


def get_charset(name: str = "standard") -> str:
    """
    Get a charset by name.
    
    Args:
        name: The name of the charset
        
    Returns:
        The charset string
        
    Raises:
        ValueError: If charset name is not found
    """
    if name.lower() not in CHARSETS:
        available = ", ".join(CHARSETS.keys())
        raise ValueError(f"Unknown charset '{name}'. Available: {available}")
    return CHARSETS[name.lower()]


def list_charsets() -> list:
    """
    Get list of all available charset names.
    
    Returns:
        List of charset names
    """
    return list(CHARSETS.keys())
