#!/usr/bin/env python3
"""
Tests for ASCII character sets.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ascii_charsets import get_charset, list_charsets, CHARSETS


def test_get_charset_standard():
    """Test getting standard charset."""
    charset = get_charset("standard")
    assert isinstance(charset, str)
    assert len(charset) > 0


def test_get_charset_all():
    """Test getting all available charsets."""
    for charset_name in list_charsets():
        charset = get_charset(charset_name)
        assert isinstance(charset, str)
        assert len(charset) > 0


def test_get_charset_invalid():
    """Test getting invalid charset raises error."""
    try:
        get_charset("invalid_charset_name")
        assert False, "Should have raised ValueError"
    except ValueError:
        pass


def test_list_charsets():
    """Test listing available charsets."""
    charsets = list_charsets()
    assert isinstance(charsets, list)
    assert len(charsets) > 0
    assert "standard" in charsets
    assert "simple" in charsets


def test_charsets_dict():
    """Test charsets dictionary."""
    assert isinstance(CHARSETS, dict)
    assert "standard" in CHARSETS
    assert "simple" in CHARSETS
    assert "block" in CHARSETS


if __name__ == "__main__":
    test_get_charset_standard()
    test_get_charset_all()
    test_get_charset_invalid()
    test_list_charsets()
    test_charsets_dict()
    print("All tests passed!")
