# AudioBookzOrganizer

AudioBookzOrganizer is a Python utility that renames and organizes your audiobook collection. It can sort folders by author or other metadata using a configurable naming scheme. The goal is to create a clean, navigable library for large audiobook collections.

## Features

* **Metadata Parsing**: Extracts basic information such as author and title from common folder naming schemes.
* **File Renaming**: Renames folders based on a customizable naming scheme (default: `"{title} - {author}"`).
* **Folder Organization**: Optionally creates sub‑folders (e.g. by author) and moves audiobook folders into them.
* **Command-Line Interface**: Supports dry runs and fully automated execution.

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/itsbryanman/AudioBookzOrganizer.git
   cd AudioBookzOrganizer
   ```
2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the script in dry-run mode to see what changes would be made:

```bash
python Organize.py --input /path/to/audiobooks
```

Add `--commit` to actually rename and move folders. You can also specify a different output directory, naming convention, and folder hierarchy.

```bash
python Organize.py -i /input/path -o /output/path \
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

Contributions are welcome! Feel free to open issues or pull requests with improvements.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
