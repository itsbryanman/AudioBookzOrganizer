"""Core filesystem operations for organizing audiobooks."""

from __future__ import annotations

from pathlib import Path

from .parser import parse_folder


def organize_audiobooks(
    audiobook_dir: Path,
    output_dir: Path,
    naming: str,
    structure: list[str],
    commit: bool,
) -> None:
    """Scan ``audiobook_dir`` and organize audiobook folders.

    Parameters
    ----------
    audiobook_dir: Path
        Directory containing unorganized audiobook folders.
    output_dir: Path
        Destination directory for organized audiobooks.
    naming: str
        Naming convention for final folder names.
    structure: list[str]
        Folder hierarchy expressed as a list of audiobook attributes.
    commit: bool
        If ``True``, perform changes; otherwise print actions only.
    """

    print("\nScanning for folders to rename and organize...")
    processed_count = 0

    for folder_path in audiobook_dir.iterdir():
        if not folder_path.is_dir():
            print(f"Skipping file: {folder_path.name}")
            continue

        audiobook = parse_folder(folder_path)
        if not audiobook:
            print(f"Skipping folder: {folder_path.name} (No matching pattern)")
            continue

        target_path = audiobook.get_target_path(output_dir, naming, structure)

        if not commit:
            print(f"Would move: {folder_path} -> {target_path}")
        else:
            if target_path.exists():
                print(f"Skipping: {folder_path} (Target exists: {target_path})")
                continue
            try:
                target_path.parent.mkdir(parents=True, exist_ok=True)
                folder_path.rename(target_path)
                print(f"Moved: {folder_path} -> {target_path}")
            except OSError as e:
                print(f"Error moving {folder_path}: {e}")

        processed_count += 1

    msg = "Operation complete" if commit else "Dry run complete"
    print(f"\n{msg}. {processed_count} folders processed.")
