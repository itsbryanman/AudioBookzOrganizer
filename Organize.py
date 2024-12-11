import os
import re
from pathlib import Path

# Supported audiobook file extensions
SUPPORTED_EXTENSIONS = {".mp3", ".m4b", ".aac", ".wav", ".ogg"}

# Define a pattern to match the file naming convention.
# Example format: "Author - Title (Year)"
FILENAME_PATTERN = re.compile(r"(?P<author>[^-]+) - (?P<title>.+?) \((?P<year>\d{4})\)")

def parse_filename(filename):
    """
    Parses the filename using a regular expression pattern to extract metadata.
    Returns a dictionary with author, title, and year if matched.
    """
    match = FILENAME_PATTERN.match(filename)
    if match:
        return match.groupdict()
    else:
        return None

def rename_and_organize(file_path, metadata, audiobook_dir, dry_run=True):
    """
    Renames and organizes an audiobook file based on parsed metadata.
    Format: "Title - Author"
    """
    author = metadata.get("author", "Unknown Author").strip()
    title = metadata.get("title", "Unknown Title").strip()

    # Customizable naming convention
    new_name = f"{title} - {author}{file_path.suffix}"

    # Define target directory structure
    target_dir = audiobook_dir / author
    target_path = target_dir / new_name

    # Print the change (dry run or real run)
    if dry_run:
        print(f"Would rename and move: {file_path} -> {target_path}")
    else:
        target_dir.mkdir(parents=True, exist_ok=True)
        file_path.rename(target_path)

def main():
    # Prompt the user to input the audiobook directory
    audiobook_dir = Path(input("Where are your audiobooks at? (Enter the full path): ").strip())
    
    if not audiobook_dir.exists() or not audiobook_dir.is_dir():
        print("Invalid path. Please provide a valid directory.")
        return
    
    # Dry-run mode
    print("\nScanning for files to rename and organize...")
    renamed_files = []
    for audio_file in audiobook_dir.glob("*"):
        if audio_file.suffix.lower() in SUPPORTED_EXTENSIONS:
            metadata = parse_filename(audio_file.stem)
            if metadata:
                rename_and_organize(audio_file, metadata, audiobook_dir, dry_run=True)
                renamed_files.append(audio_file)
            else:
                print(f"Skipping file: {audio_file.name} due to unmatched pattern")
        else:
            print(f"Skipping unsupported file type: {audio_file.name}")

    # Summary
    print(f"\nDry run complete. {len(renamed_files)} files would be renamed and organized.")

    # Ask for confirmation
    confirm = input("\nDo you want to commit these changes? (yes/no): ").strip().lower()
    if confirm == "yes":
        print("\nCommitting changes...")
        for audio_file in renamed_files:
            metadata = parse_filename(audio_file.stem)
            if metadata:
                rename_and_organize(audio_file, metadata, audiobook_dir, dry_run=False)
        print("Renaming and organization complete.")
    else:
        print("\nNo changes were made. Exiting.")

if __name__ == "__main__":
    main()
