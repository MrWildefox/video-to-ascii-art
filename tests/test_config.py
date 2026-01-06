#!/usr/bin/env python3
"""
Tests for configuration.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config


def test_config_values():
    """Test that config values are set."""
    assert hasattr(config, 'DEFAULT_WIDTH')
    assert hasattr(config, 'DEFAULT_HEIGHT')
    assert hasattr(config, 'DEFAULT_CHARSET')
    assert hasattr(config, 'DEFAULT_SPEED')


def test_config_types():
    """Test that config values have correct types."""
    assert isinstance(config.DEFAULT_WIDTH, int)
    assert isinstance(config.DEFAULT_HEIGHT, int)
    assert isinstance(config.DEFAULT_CHARSET, str)
    assert isinstance(config.DEFAULT_SPEED, (int, float))
    assert isinstance(config.ENABLE_COLOR, bool)


def test_config_ranges():
    """Test that config values are in valid ranges."""
    assert config.DEFAULT_WIDTH > 0
    assert config.DEFAULT_HEIGHT > 0
    assert config.DEFAULT_SPEED > 0
    assert 0 <= config.ASPECT_RATIO_CORRECTION <= 1


if __name__ == "__main__":
    test_config_values()
    test_config_types()
    test_config_ranges()
    print("All tests passed!")
