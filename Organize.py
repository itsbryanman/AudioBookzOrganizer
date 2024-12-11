import os
import re
from pathlib import Path

# Define a pattern to match the file naming convention.
# Adjust this pattern to match your file naming structure.
# Example format: "Author - Series - Title (Year)"
FILENAME_PATTERN = re.compile(r"(?P<author>[^-]+) - (?P<series>[^-]+) - (?P<title>.+?) \((?P<year>\d{4})\)")

# Supported audiobook file extensions
SUPPORTED_EXTENSIONS = {".mp3", ".m4b", ".aac", ".wav", ".ogg"}

def parse_filename(filename):
    """
    Parses the filename using a regular expression pattern to extract metadata.
    Returns a dictionary with author, series, title, and year if matched.
    """
    match = FILENAME_PATTERN.match(filename)
    if match:
        return match.groupdict()
    else:
        print(f"Filename pattern did not match for file: {filename}")
        return None

def rename_and_organize(file_path, metadata, audiobook_dir):
    """
    Renames and organizes an audiobook file based on parsed metadata.
    """
    author = metadata.get("author", "Unknown Author").strip()
    title = metadata.get("title", "Unknown Title").strip()
    year = metadata.get("year", "Unknown Year").strip()
    series = metadata.get("series", "Standalone").strip()

    # Customizable naming convention
    new_name = f"{author} - {series} - {title} ({year}){file_path.suffix}"

    # Define target directory structure
    target_dir = audiobook_dir / author / series
    target_dir.mkdir(parents=True, exist_ok=True)

    # Rename and move file
    target_path = target_dir / new_name
    file_path.rename(target_path)
    print(f"Renamed and moved {file_path.name} to {target_path}")

def main():
    # Prompt the user to input the audiobook directory
    audiobook_dir = Path(input("Where are your audiobooks at? (Enter the full path): ").strip())
    
    if not audiobook_dir.exists() or not audiobook_dir.is_dir():
        print("Invalid path. Please provide a valid directory.")
        return
    
    renamed_count = 0

    # Scan for audiobook files in the directory with supported extensions
    for audio_file in audiobook_dir.glob("*"):
        if audio_file.suffix.lower() in SUPPORTED_EXTENSIONS:
            metadata = parse_filename(audio_file.stem)
            if metadata:
                rename_and_organize(audio_file, metadata, audiobook_dir)
                renamed_count += 1
            else:
                print(f"Skipping file: {audio_file.name} due to unmatched pattern")
        else:
            print(f"Skipping unsupported file type: {audio_file.name}")
    
    # Print summary
    print(f"\nDone! Renamed and organized {renamed_count} audiobooks.")

if __name__ == "__main__":
    main()
