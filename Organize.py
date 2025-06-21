import argparse
import os
import re
from pathlib import Path

import mutagen

# Define a pattern to match common folder naming conventions.
# Handles formats like:
# - "Author - Title"
# - "Title - Author"
FOLDERNAME_PATTERNS = [
    re.compile(r"(?P<author>[^-]+) - (?P<title>.+)"),  # Format: Author - Title
    re.compile(r"(?P<title>.+) - (?P<author>[^-]+)"),  # Format: Title - Author
]

def parse_foldername(foldername):
    """Parse the folder name to extract metadata."""
    for pattern in FOLDERNAME_PATTERNS:
        match = pattern.match(foldername)
        if match:
            return match.groupdict()
    return {}

def extract_metadata_from_files(folder_path):
    """Scan for audio files and extract metadata using mutagen."""
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith((
                '.mp3',
                '.m4a',
                '.m4b',
                '.flac',
            )):
                try:
                    audio = mutagen.File(os.path.join(root, file))
                    if audio:
                        title = audio.get('album', [None])[0]
                        author = audio.get('artist', [None])[0]
                        if title and author:
                            return {'title': str(title), 'author': str(author)}
                except Exception as e:  # pragma: no cover - best effort
                    print(f"Could not read metadata from {file}: {e}")
    return {}

def build_target_path(base_dir, metadata, naming, structure):
    """Build the destination path based on structure and naming."""
    parts = []
    for field in structure:
        value = metadata.get(field, f"Unknown {field.title()}").strip()
        parts.append(value)
    target_base = base_dir.joinpath(*parts)

    author = metadata.get("author", "Unknown Author").strip()
    title = metadata.get("title", "Unknown Title").strip()
    folder_name = naming.format(author=author, title=title)
    return target_base / folder_name

def rename_and_organize_folder(folder_path, metadata, output_dir, naming, structure, dry_run=True):
    target_path = build_target_path(output_dir, metadata, naming, structure)

    if dry_run:
        print(f"Would move: {folder_path} -> {target_path}")
    else:
        target_path.parent.mkdir(parents=True, exist_ok=True)
        if not target_path.exists():
            folder_path.rename(target_path)
            print(f"Moved: {folder_path} -> {target_path}")
        else:
            print(f"Skipping: {folder_path} (Target exists)")

def organize_audiobooks(audiobook_dir, output_dir=None, naming="{title} - {author}", structure=None, commit=False):
    audiobook_dir = Path(audiobook_dir)
    output_dir = Path(output_dir) if output_dir else audiobook_dir
    structure = [s.strip() for s in (structure or []) if s.strip()]

    print("\nScanning for folders to rename and organize...")
    processed = []
    for folder in audiobook_dir.iterdir():
        if folder.is_dir():
            metadata = extract_metadata_from_files(folder)

            if not metadata:
                metadata = parse_foldername(folder.name)

            if metadata:
                rename_and_organize_folder(
                    folder,
                    metadata,
                    output_dir,
                    naming,
                    structure,
                    dry_run=not commit,
                )
                processed.append(folder)
            else:
                print(f"Skipping folder: {folder.name} (Could not determine metadata)")
        else:
            print(f"Skipping file: {folder.name} (Not a folder)")

    msg = "Operation complete" if commit else "Dry run complete"
    print(f"\n{msg}. {len(processed)} folders processed.")

def parse_args():
    parser = argparse.ArgumentParser(description="Organize audiobook folders")
    parser.add_argument("--input", "-i", required=False, help="Directory with audiobook folders")
    parser.add_argument("--output", "-o", help="Directory to place organized folders")
    parser.add_argument("--naming-convention", "-n", default="{title} - {author}", help="Folder naming pattern")
    parser.add_argument("--folder-structure", "-s", default="", help="Comma separated hierarchy (e.g. author)")
    parser.add_argument("--commit", action="store_true", help="Apply changes instead of dry run")
    return parser.parse_args()

def main():
    args = parse_args()

    audiobook_dir = Path(args.input) if args.input else Path(input("Where are your audiobook folders at? (Enter the full path): ").strip())
    if not audiobook_dir.exists() or not audiobook_dir.is_dir():
        print("Invalid path. Please provide a valid directory.")
        return

    output_dir = Path(args.output) if args.output else audiobook_dir
    structure = args.folder_structure.split(',') if args.folder_structure else []

    organize_audiobooks(
        audiobook_dir=audiobook_dir,
        output_dir=output_dir,
        naming=args.naming_convention,
        structure=structure,
        commit=args.commit,
    )

if __name__ == "__main__":
    main()
