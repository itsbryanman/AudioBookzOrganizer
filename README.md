

# AudioBookzOrganizer

[](https://www.google.com/search?q=https://github.com/itsbryanman/AudioBookzOrganizer/actions/workflows/main.yml)
[](https://www.google.com/search?q=https://codecov.io/gh/itsbryanman/AudioBookzOrganizer)
[](https://opensource.org/licenses/MIT)
[](https://github.com/psf/black)

> A powerful and flexible Python utility for intelligently renaming and organizing your audiobook collection, complete with a clean Terminal User Interface (TUI).

-----

## About The Project

Tired of manually sifting through a chaotic mess of audiobook files? `AudioBookzOrganizer` automates the entire process. It extracts metadata, fetches additional details from the Google Books API, and reorganizes your library according to your exact specifications. Its interactive TUI provides a crystal-clear overview and full control over the process, ensuring your collection is always clean, navigable, and exactly how you want it.

### The TUI Experience

The script features an interactive Terminal User Interface that gives you a preview of all planned changes. You can review and confirm every move before a single file is touched.

```

┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                              📚 AudioBookzOrganizer [PREVIEW]                             │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│    STATUS    |    SOURCE PATH                               |    DESTINATION PATH       │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│  ✅ RENAME   |  /in/Project Hail Mary/                    |  /out/Sci-Fi/Weir, Andy/Project Hail Mary - Andy Weir/
│  ✅ RENAME   |  /in/Dune - F Herbert/                     |  /out/Sci-Fi/Herbert, Frank/Dune - Frank Herbert/
│  ⚠️  NO TAGS  |  /in/audiobook_123/                        |  (skipping)
│  ✅ RENAME   |  /in/Stephen King - The Stand/             |  /out/Horror/King, Stephen/The Stand - Stephen King/
└─────────────────────────────────────────────────────────────────────────────────────────┘
            [C]ommit changes | [A]bort
```

-----

## Features

  - **Advanced Metadata Extraction**: Reads author, title, and other tags directly from audio files (`MP3`, `M4A`, `M4B`). Falls back to folder names if tags are missing.
  - **Google Books Integration**: Enriches your library by automatically fetching metadata like `genre` and `publication year`.
  - **Interactive TUI**: A clean, intuitive Terminal User Interface to visualize and confirm changes before they are made.
  - **Customizable Naming Schemes**: Define your own folder and file naming conventions using a wide range of metadata placeholders (e.g., `{title} - {author}`).
  - **Flexible Folder Organization**: Organize your audiobooks into a nested folder structure based on any combination of metadata fields (e.g., `genre`, `author`).
  - **High-Performance Processing**: Utilizes a concurrent thread pool to scan and process large libraries with maximum speed and efficiency.
  - **Dry-Run Mode**: By default, the script performs a dry run, allowing you to preview all proposed changes without affecting your files.

-----

## Getting Started

### Prerequisites

  - Python 3.7+
  - An optional API key for the **Google Books API** for significantly increased request quotas.

### Installation

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/itsbryanman/AudioBookzOrganizer.git
    cd AudioBookzOrganizer
    ```
2.  **Install dependencies:**
    ```sh
    # We recommend using a virtual environment
    python -m venv venv
    source venv/bin/activate

    # Install the package in editable mode with testing extras
    pip install -e .[test]
    ```

-----

## Usage

`AudioBookzOrganizer` is run from the command line and offers a range of flags to customize the organization of your library.

### Basic Usage

To launch the TUI and see a preview of the changes without modifying any files, run the organizer in **dry-run mode** (the default behavior):

```sh
organize-audiobooks --input /path/to/your/audiobooks
```

### Advanced Usage

To commit the changes and organize your audiobooks into a new directory with a `genre/author` folder structure:

```sh
organize-audiobooks -i /input/path -o /output/path \
  --naming-convention "{author} - {title}" \
  --folder-structure genre,author \
  --fetch-metadata --api-key YOUR_GOOGLE_BOOKS_API_KEY --commit
```

### Command-Line Options

| Flag | Alias | Description | Default |
| :--- | :---: | :--- | :--- |
| `--input` | `-i` | Directory containing the audiobook folders to process. | **Required** |
| `--output` | `-o` | Directory where organized folders will be placed. | Same as input |
| `--naming-convention` | `-n` | Pattern for the final folder name. See placeholders below. | `{title} - {author}` |
| `--folder-structure` | `-s` | Comma-separated list for subdirectories (e.g., `genre,author`).| `     ` (none) |
| `--fetch-metadata` | | Fetch metadata from Google Books API to fill in missing tags. | `False` |
| `--api-key` | | Your Google Books API key for a higher request quota. | `     ` (none) |
| `--commit` | | Apply the changes. Without this flag, the script performs a dry run. | `False` |

**Available Placeholders:** `{author}`, `{title}`, `{genre}`, `{year}`

-----

## Contributing

Contributions are what make the open-source community an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

Please read [CONTRIBUTING.md](https://www.google.com/search?q=CONTRIBUTING.md) for guidelines on how to contribute to the project.

-----

## License

This project is licensed under the MIT License. See the [LICENSE](https://www.google.com/search?q=LICENSE) file for more information.
