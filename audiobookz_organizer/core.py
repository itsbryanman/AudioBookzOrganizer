"""Core filesystem operations for organizing audiobooks."""

from __future__ import annotations

from pathlib import Path
import concurrent.futures
import time
from contextlib import nullcontext

from .parser import parse_folder
from .metadata import extract_metadata_from_folder, infer_genre_from_text
from .models import Audiobook
from .fetcher import fetch_book_details
from .tagger import update_audiobook_tags
from .logger import get_logger
from .benchmark import get_benchmark_collector, TimedOperation, reset_benchmark_collector


class AudioBookProcessError(Exception):
    """Raised when an expected error occurs during audiobook processing."""
    pass


def organize_audiobooks(
    audiobook_dir: Path,
    output_dir: Path,
    naming: str,
    structure: list[str],
    commit: bool,
    fetch_metadata: bool = False,
    api_key: str | None = None,
    use_cache: bool = True,
    write_tags: bool = False,
    enable_benchmark: bool = False,
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
    fetch_metadata: bool
        When ``True``, attempt to fetch genre and year via the Google Books API.
    api_key: str | None
        Google Books API key to use when fetching metadata.
    """

    logger = get_logger()
    logger.log_operation_start(audiobook_dir, output_dir, not commit)
    
    # Setup benchmarking
    benchmark_collector = None
    if enable_benchmark:
        reset_benchmark_collector()
        benchmark_collector = get_benchmark_collector()
    
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
                api_key,
                use_cache,
                write_tags,
                enable_benchmark,
            ): folder
            for folder in folders_to_process
        }

        for future in concurrent.futures.as_completed(futures):
            folder = futures[future]
            try:
                message = future.result()
                if message:
                    print(message)
                    logger.log_folder_processed(folder, message)
                    if "MOVED" in message or "DRY-RUN" in message:
                        processed_count += 1
            except AudioBookProcessError as exc:
                print(str(exc))
                logger.log_error(str(exc))

    msg = "Operation complete" if commit else "Dry run complete"
    print(f"\n{msg}. {processed_count} folders processed.")
    logger.log_operation_end(processed_count, not commit)
    
    # Print benchmark results
    if enable_benchmark and benchmark_collector:
        benchmark_collector.finish_benchmark()
        benchmark_collector.print_summary()
        benchmark_collector.print_detailed_report()


def _process_folder(
    folder_path: Path,
    output_dir: Path,
    naming: str,
    structure: list[str],
    commit: bool,
    fetch_metadata: bool,
    api_key: str | None,
    use_cache: bool,
    write_tags: bool,
    enable_benchmark: bool,
) -> str:
    logger = get_logger()
    
    # Start overall timing for this folder
    folder_start_time = time.time()
    
    # Extract metadata with timing
    with TimedOperation("metadata_extraction", folder_path.name) if enable_benchmark else nullcontext():
        metadata = extract_metadata_from_folder(folder_path)
    
    audiobook: Audiobook | None = None

    if metadata:
        audiobook = Audiobook(
            source_path=folder_path,
            author=metadata.get("author", "Unknown Author"),
            title=metadata.get("title", "Unknown Title"),
            genre=metadata.get("genre", "Unknown Genre"),
            year=metadata.get("year", "0000"),
        )
    else:
        audiobook = parse_folder(folder_path)

    if not audiobook:
        return f"SKIPPED: {folder_path.name} (Could not determine metadata)"

    if fetch_metadata:
        details = fetch_book_details(audiobook.title, audiobook.author, api_key, use_cache)
        if details:
            audiobook.genre = details.get("genre", audiobook.genre)
            audiobook.year = details.get("year", audiobook.year)
            logger.log_metadata_fetched(audiobook.title, audiobook.author, True)
        else:
            logger.log_metadata_fetched(audiobook.title, audiobook.author, False)
    
    # If genre is still unknown, try to infer it from title/author
    if audiobook.genre == "Unknown Genre":
        inferred_genre = infer_genre_from_text(audiobook.title, audiobook.author)
        if inferred_genre != "Unknown Genre":
            audiobook.genre = inferred_genre
            logger.log_genre_inference(audiobook.title, audiobook.author, inferred_genre)

    # Update tags if requested
    if write_tags:
        tag_stats = update_audiobook_tags(audiobook, dry_run=not commit)
        if tag_stats["files_updated"] > 0:
            tag_msg = f"Updated tags for {tag_stats['files_updated']} files"
            if not commit:
                tag_msg = f"DRY-RUN: Would update tags for {tag_stats['files_updated']} files"
        else:
            tag_msg = "No tag updates needed"
    
    target_path = audiobook.get_target_path(output_dir, naming, structure)

    if target_path.exists():
        return f"SKIPPED: {folder_path.name} (Target exists)"

    if not commit:
        move_msg = f"DRY-RUN: Would move {folder_path} -> {target_path}"
        if write_tags:
            return f"{move_msg} | {tag_msg}"
        return move_msg

    try:
        target_path.parent.mkdir(parents=True, exist_ok=True)
        folder_path.rename(target_path)
        move_msg = f"MOVED: {folder_path} -> {target_path}"
        if write_tags:
            return f"{move_msg} | {tag_msg}"
        return move_msg
    except OSError as e:
        raise AudioBookProcessError(f"ERROR: Failed to move {folder_path}: {e}")
