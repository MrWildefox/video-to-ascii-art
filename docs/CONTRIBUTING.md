# Contributing to Video to ASCII Art

Thank you for considering contributing! This document provides guidelines and instructions.

## Code of Conduct

Be respectful, inclusive, and constructive in all interactions.

## How to Contribute

### Reporting Bugs

1. Check existing issues to avoid duplicates
2. Create a new issue with:
   - Clear title describing the bug
   - Steps to reproduce
   - Expected vs actual behavior
   - System info (OS, Python version, etc.)
   - Error messages/logs

### Suggesting Features

1. Check existing issues/discussions
2. Create an issue with:
   - Clear description of the feature
   - Use cases and benefits
   - Example usage if applicable
   - Possible implementation approaches

### Code Contributions

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/my-feature`
3. **Make** your changes following the style guide
4. **Test** your changes thoroughly
5. **Commit** with clear messages: `git commit -m 'Add my feature'`
6. **Push** to your fork: `git push origin feature/my-feature`
7. **Create** a Pull Request with description

## Style Guide

### Python Style

- Follow PEP 8
- Use type hints for functions
- Document with docstrings (Google style)
- Maximum line length: 100 characters
- Use meaningful variable names

### Example:

```python
def convert_frame(frame: np.ndarray, width: int = 120) -> str:
    """
    Convert a video frame to ASCII art.
    
    Args:
        frame: Input frame as numpy array (BGR or grayscale)
        width: Output width in characters
        
    Returns:
        ASCII art as string
        
    Raises:
        ValueError: If frame is invalid
    """
```

### Commit Messages

- Start with verb: "Add", "Fix", "Improve", "Refactor"
- Keep first line under 72 characters
- Use present tense: "Add feature" not "Added feature"
- Reference issues: "Fix #123"

Good examples:
- `Add color support for ASCII output`
- `Fix frame timing issue with high FPS videos`
- `Refactor ASCIIConverter for better performance`

## Testing

Before submitting:

1. Test with multiple video formats (MP4, AVI, MOV)
2. Test with different charset options
3. Test with different widths (60, 100, 150)
4. Ensure no regressions in existing functionality
5. Add tests for new features

### Running Tests

```bash
python -m pytest tests/
```

## Documentation

- Update README.md if adding/changing features
- Add docstrings to all functions
- Update ARCHITECTURE.md for structural changes
- Add examples in docs/ if relevant

## Pull Request Process

1. **Fill out** the PR template completely
2. **Link** related issues
3. **Describe** your changes and why
4. **Show** any relevant output/screenshots
5. **Request** review from maintainers

PR checklist:
- [ ] Code follows style guide
- [ ] Documentation updated
- [ ] Tests added/passed
- [ ] No breaking changes
- [ ] Commits are clean and descriptive

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR-USERNAME/video-to-ascii-art.git
cd video-to-ascii-art

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or .\venv\Scripts\activate on Windows

# Install in development mode
pip install -e .
pip install -r requirements-dev.txt

# Make your changes
# Test
python -m pytest

# Format code
black .
flake8 .
```

## Areas for Contribution

### High Priority
- [ ] Color output implementation
- [ ] Audio synchronization
- [ ] GPU acceleration
- [ ] Windows cmd.exe compatibility

### Medium Priority
- [ ] Additional character sets
- [ ] Effect filters (edge detection, etc.)
- [ ] Performance optimizations
- [ ] Better error handling

### Low Priority
- [ ] Additional documentation
- [ ] Example videos
- [ ] Internationalization
- [ ] Alternative output formats

## Questions?

Feel free to:
- Open an issue with tag "question"
- Start a discussion in the Discussions tab
- Email the maintainer

## Recognition

Contributors will be:
- Added to CONTRIBUTORS.md
- Mentioned in release notes
- Thanked in README.md

Thank you for contributing! 🎉
