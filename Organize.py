import os
import re
from pathlib import Path

# Define a pattern to match common folder naming conventions.
# Handles formats like:
# - "Author - Title"
# - "Title - Author"
FOLDERNAME_PATTERNS = [
    re.compile(r"(?P<author>[^-]+) - (?P<title>.+)"),  # Format: Author - Title
    re.compile(r"(?P<title>.+) - (?P<author>[^-]+)"),  # Format: Title - Author
]

def parse_foldername(foldername):
    """
    Parses the folder name using regular expression patterns to extract metadata.
    Returns a dictionary with author and title if matched.
    """
    for pattern in FOLDERNAME_PATTERNS:
        match = pattern.match(foldername)
        if match:
            return match.groupdict()
    return None

def rename_and_organize_folder(folder_path, metadata, audiobook_dir, dry_run=True):
    """
    Renames and organizes an audiobook folder based on parsed metadata.
    Format: "Title - Author"
    """
    author = metadata.get("author", "Unknown Author").strip()
    title = metadata.get("title", "Unknown Title").strip()

    # Customizable naming convention for folders
    new_folder_name = f"{title} - {author}"

    # Define the target folder path
    target_path = audiobook_dir / new_folder_name

    # Print the change (dry run or real run)
    if dry_run:
        print(f"Would rename and move: {folder_path} -> {target_path}")
    else:
        if not target_path.exists():
            folder_path.rename(target_path)
            print(f"Renamed and moved: {folder_path} -> {target_path}")
        else:
            print(f"Skipping: {folder_path} (Target folder already exists)")

def main():
    # Prompt the user to input the audiobook directory
    audiobook_dir = Path(input("Where are your audiobook folders at? (Enter the full path): ").strip())
    
    if not audiobook_dir.exists() or not audiobook_dir.is_dir():
        print("Invalid path. Please provide a valid directory.")
        return

    # Dry-run mode
    print("\nScanning for folders to rename and organize...")
    renamed_folders = []
    for folder in audiobook_dir.iterdir():
        if folder.is_dir():
            metadata = parse_foldername(folder.name)
            if metadata:
                rename_and_organize_folder(folder, metadata, audiobook_dir, dry_run=True)
                renamed_folders.append(folder)
            else:
                print(f"Skipping folder: {folder.name} (No matching pattern)")
        else:
            print(f"Skipping file: {folder.name} (Not a folder)")

    # Summary
    print(f"\nDry run complete. {len(renamed_folders)} folders would be renamed and organized.")

    # Ask for confirmation
    confirm = input("\nDo you want to commit these changes? (yes/no): ").strip().lower()
    if confirm == "yes":
        print("\nCommitting changes...")
        for folder in renamed_folders:
            metadata = parse_foldername(folder.name)
            if metadata:
                rename_and_organize_folder(folder, metadata, audiobook_dir, dry_run=False)
        print("Folder renaming and organization complete.")
    else:
        print("\nNo changes were made. Exiting.")

if __name__ == "__main__":
    main()
