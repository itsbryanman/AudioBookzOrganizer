"""Core filesystem operations for organizing audiobooks."""

from __future__ import annotations

from pathlib import Path
import concurrent.futures

from .parser import parse_folder
from .metadata import extract_metadata_from_folder
from .models import Audiobook
from .fetcher import fetch_book_details


def organize_audiobooks(
    audiobook_dir: Path,
    output_dir: Path,
    naming: str,
    structure: list[str],
    commit: bool,
    fetch_metadata: bool = False,
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

    folders_to_process = [p for p in audiobook_dir.iterdir() if p.is_dir()]
    processed_count = 0

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {
            executor.submit(
                _process_folder,
                folder,
                output_dir,
                naming,
                structure,
                commit,
                fetch_metadata,
            ): folder
            for folder in folders_to_process
        }

        for future in concurrent.futures.as_completed(futures):
            folder = futures[future]
            try:
                message = future.result()
                if message:
                    print(message)
                    if "MOVED" in message or "DRY-RUN" in message:
                        processed_count += 1
            except Exception as exc:
                print(f"ERROR: An exception occurred while processing {folder.name}: {exc}")

    msg = "Operation complete" if commit else "Dry run complete"
    print(f"\n{msg}. {processed_count} folders processed.")


def _process_folder(
    folder_path: Path,
    output_dir: Path,
    naming: str,
    structure: list[str],
    commit: bool,
    fetch_metadata: bool,
) -> str:
    metadata = extract_metadata_from_folder(folder_path)
    audiobook: Audiobook | None = None

    if metadata:
        audiobook = Audiobook(
            source_path=folder_path,
            author=metadata.get("author", "Unknown Author"),
            title=metadata.get("title", "Unknown Title"),
        )
    else:
        audiobook = parse_folder(folder_path)

    if not audiobook:
        return f"SKIPPED: {folder_path.name} (Could not determine metadata)"

    if fetch_metadata:
        details = fetch_book_details(audiobook.title, audiobook.author)
        if details:
            audiobook.genre = details.get("genre", audiobook.genre)
            audiobook.year = details.get("year", audiobook.year)

    target_path = audiobook.get_target_path(output_dir, naming, structure)

    if not commit:
        return f"DRY-RUN: Would move {folder_path} -> {target_path}"

    if target_path.exists():
        return f"SKIPPED: {folder_path.name} (Target exists)"

    try:
        target_path.parent.mkdir(parents=True, exist_ok=True)
        folder_path.rename(target_path)
        return f"MOVED: {folder_path} -> {target_path}"
    except OSError as e:
        return f"ERROR: Failed to move {folder_path}: {e}"
