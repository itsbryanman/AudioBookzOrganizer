# AudioBookzOrganizer

AudioBookzOrganizer is a Python script that renames, organizes, and enriches your audiobook collection by fetching metadata from Audible. It sorts files by author, series, or genre, applies custom naming conventions, and creates a clean, navigable library.

## Features

* **Metadata Fetching**: Automatically fetches audiobook metadata from [Source, e.g., Audible].
* **File Renaming**: Renames files based on a customizable naming scheme (e.g., `Author - Series - Book Title.mp3`).
* **Folder Organization**: Organizes files into a directory structure based on author, series, genre, or other metadata.
* **GUI Interface**: A simple  but complex graphical user interface for easy use.
* **Command-Line Interface**: For automation and scripting.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/itsbryanman/AudioBookzOrganizer.git](https://github.com/itsbryanman/AudioBookzOrganizer.git)
    cd AudioBookzOrganizer
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *(You will need to create a `requirements.txt` file listing the Python libraries your project needs, e.g., `mutagen`, `requests`)*

## Usage

### GUI Mode

To run the application with the graphical user interface:
```bash
python gui.py
```
Then, simply select your input and output directories and click "Organize!".

### Command-Line Mode

To run the script from the command line:

```bash
python Organize.py --input <input_directory> --output <output_directory> [options]
```

**Options:**

* `--input`: The directory containing the audiobook files to organize.
* `--output`: The directory where the organized files will be saved.
* `--naming-convention`: The file naming convention (e.g., `"{author} - {title}"`).
* `--folder-structure`: The folder structure (e.g., `author,series`).

## Contributing

Contributions are welcome! If you have any ideas, suggestions, or bug reports, please open an issue or create a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.