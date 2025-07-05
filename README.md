

[![CI](https://github.com/itsbryanman/AudioBookzOrganizer/actions/workflows/main.yml/badge.svg)](https://github.com/itsbryanman/AudioBookzOrganizer/actions/workflows/main.yml)
[![codecov](https://codecov.io/gh/itsbryanman/AudioBookzOrganizer/branch/main/graph/badge.svg)](https://codecov.io/gh/itsbryanman/AudioBookzOrganizer)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

# AudioBookzOrganizer

A powerful and flexible Python utility for intelligently renaming and organizing your audiobook collection with an interactive Terminal User Interface.

## Quick Start

### Installation

```bash
git clone https://github.com/itsbryanman/AudioBookzOrganizer.git
cd AudioBookzOrganizer
pip install -e .
```

### Basic Usage

```bash
# Preview changes (dry run)
organize-audiobooks --input /path/to/audiobooks

# Apply changes
organize-audiobooks --input /path/to/audiobooks --commit
```

-----

## Features

- **Advanced Metadata Extraction**: Reads author, title, genre, and year directly from audio files (MP3, M4A, M4B, FLAC). Falls back to folder names if tags are missing.
- **Multi-Part Audiobook Detection**: Automatically detects and preserves multi-file audiobooks (discs, parts, chapters) as complete units.
- **Google Books Integration**: Enriches your library by automatically fetching metadata like genre and publication year.
- **Intelligent Metadata Caching**: Caches API results to avoid redundant requests and speed up repeated operations.
- **Robust Genre Inference**: Advanced genre detection using keyword analysis when metadata is missing.
- **Interactive Terminal UI**: Clean, intuitive interface with sorting, navigation, and detailed preview capabilities.
- **Optional Tag Editing**: Update audio file metadata tags with the `--write-tags` flag.
- **Comprehensive Logging**: Detailed logging with color-coded output and optional file logging.
- **Performance Benchmarking**: Detailed timing analysis with `--benchmark` to optimize your workflow.
- **Customizable Organization**: Define your own folder and file naming conventions using metadata placeholders.
- **High-Performance Processing**: Utilizes concurrent thread pools for maximum speed and efficiency.
- **Safe Dry-Run Mode**: Preview all changes before applying them to your files.

## Installation & Setup

### Requirements
- Python 3.8 or higher
- Optional: Google Books API key for enhanced metadata fetching

### Install from Source
```bash
git clone https://github.com/itsbryanman/AudioBookzOrganizer.git
cd AudioBookzOrganizer
pip install -e .
```

### For Development
```bash
git clone https://github.com/itsbryanman/AudioBookzOrganizer.git
cd AudioBookzOrganizer
pip install -e .[test]
```

## Usage Examples

### Basic Organization
```bash
# Preview changes (recommended first step)
organize-audiobooks --input /path/to/audiobooks

# Apply changes after preview
organize-audiobooks --input /path/to/audiobooks --commit
```

### Advanced Organization
```bash
# Organize with custom structure and fetch metadata
organize-audiobooks \
  --input /path/to/audiobooks \
  --output /path/to/organized \
  --folder-structure genre,author \
  --naming-convention "{author} - {title}" \
  --fetch-metadata \
  --api-key YOUR_API_KEY \
  --commit
```

### Performance Monitoring
```bash
# Run with benchmarking and logging
organize-audiobooks \
  --input /path/to/audiobooks \
  --benchmark \
  --log /path/to/logfile.txt \
  --commit
```

## Command-Line Options

| Flag | Alias | Description | Default |
| :--- | :---: | :--- | :--- |
| `--input` | `-i` | Directory containing audiobook folders | **Required** |
| `--output` | `-o` | Directory for organized folders | Same as input |
| `--naming-convention` | `-n` | Folder naming pattern | `{title} - {author}` |
| `--folder-structure` | `-s` | Subdirectory hierarchy (e.g., `genre,author`) | None |
| `--fetch-metadata` | | Fetch metadata from Google Books API | `False` |
| `--api-key` | | Google Books API key | None |
| `--commit` | | Apply changes (default is dry-run) | `False` |
| `--no-cache` | | Disable metadata caching | `False` |
| `--write-tags` | | Update audio file metadata tags | `False` |
| `--log` | | Log file path for detailed logging | None |
| `--benchmark` | | Enable performance benchmarking | `False` |

**Available Placeholders:** `{author}`, `{title}`, `{genre}`, `{year}`

## Advanced Features

### Multi-Part Audiobook Detection
Automatically detects and preserves:
- Multiple audio files in a folder
- Disc/Part subdirectories (e.g., "Disc 1", "Part 2")
- Numeric chapter subdirectories

### Intelligent Caching
- Local caching of Google Books API results
- Faster subsequent runs
- `--no-cache` option to force fresh requests

### Performance Analysis
- `--benchmark` flag provides detailed timing
- Per-book processing statistics
- Operation breakdown analysis
- Throughput metrics

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
