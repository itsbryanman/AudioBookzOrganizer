# AudioBookzOrganizer
[![codecov](https://codecov.io/gh/itsbryanman/AudioBookzOrganizer/branch/main/graph/badge.svg)](https://codecov.io/gh/itsbryanman/AudioBookzOrganizer)

AudioBookzOrganizer is a Python utility that renames and organizes your audiobook collection. It can sort folders by author or other metadata using a configurable naming scheme. The goal is to create a clean, navigable library for large audiobook collections.

## Features

* **Accurate Metadata Extraction**: Reads author and title metadata directly from audio files (e.g., MP3, M4A, M4B) and falls back to folder names when tags are missing.
* **File Renaming**: Renames folders based on a customizable naming scheme (default: `{title} - {author}`).
* **Folder Organization**: Optionally creates sub‑folders (e.g. by author) and moves audiobook folders into them.
* **Command-Line Interface**: Supports dry runs and fully automated execution.

## Metadata Sources

By default the organizer reads tags from the audio files themselves. If tags are missing, it falls back to parsing the folder name. Passing ``--fetch-metadata`` enables online lookups through the Google Books API for genre and publication year.

## Performance

Folders are processed concurrently using a thread pool so large libraries are scanned quickly.

## Advanced Usage

The organizer can create nested folder hierarchies using any combination of available metadata fields. For example:

```bash
organize-audiobooks -i ./in -o ./out --folder-structure genre,author --fetch-metadata --commit
```


## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/itsbryanman/AudioBookzOrganizer.git
   cd AudioBookzOrganizer
   ```
2. **Install dependencies**
   ```bash
   pip install -e .[test]
   ```

## Usage

Run the organizer in dry-run mode to see what changes would be made:

```bash
organize-audiobooks --input /path/to/audiobooks
```

Add `--commit` to actually rename and move folders. You can also specify a different output directory, naming convention, and folder hierarchy.

```bash
organize-audiobooks -i /input/path -o /output/path \
  --naming-convention "{author} - {title}" \
  --folder-structure author --commit
```

### Options

* `--input` / `-i`: Directory containing the audiobook folders.
* `--output` / `-o`: Directory where organized folders will be placed. Defaults to the input directory.
* `--naming-convention` / `-n`: Pattern for the folder name. Supported placeholders: `{author}`, `{title}`.
* `--folder-structure` / `-s`: Comma-separated list of metadata fields to use as subdirectories (e.g. `author`).
* `--commit`: Apply changes. Without this flag, the script performs a dry run.

## Contributing

Please read [CONTRIBUTING](CONTRIBUTING.md) for guidelines on how to contribute.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
