"""Command-line interface for the organizer."""

from __future__ import annotations

import argparse
from pathlib import Path

from .core import organize_audiobooks
from .logger import setup_logger


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Organize audiobook folders")
    parser.add_argument("--input", "-i", required=False, help="Directory with audiobook folders")
    parser.add_argument("--output", "-o", help="Directory to place organized folders")
    parser.add_argument(
        "--naming-convention",
        "-n",
        default="{title} - {author}",
        help="Folder naming pattern",
    )
    parser.add_argument(
        "--folder-structure",
        "-s",
        default="",
        help="Comma separated hierarchy (e.g. author)",
    )
    parser.add_argument("--commit", action="store_true", help="Apply changes instead of dry run")
    parser.add_argument(
        "--fetch-metadata",
        action="store_true",
        help="Fetch additional metadata from online sources",
    )
    parser.add_argument("--api-key", help="Google Books API key for metadata fetching")
    parser.add_argument("--no-cache", action="store_true", help="Disable metadata caching")
    parser.add_argument("--write-tags", action="store_true", help="Update audio file metadata tags")
    parser.add_argument("--log", help="Log file path for detailed logging")
    parser.add_argument("--benchmark", action="store_true", help="Enable performance benchmarking")
    return parser.parse_args()


def main() -> None:
    """Entry point for the CLI."""
    args = parse_args()
    
    # Setup logging
    log_file = Path(args.log) if args.log else None
    setup_logger(log_file, enable_colors=True)

    audiobook_dir = Path(args.input) if args.input else Path(input("Where are your audiobook folders at? (Enter the full path): ").strip())
    if not audiobook_dir.exists() or not audiobook_dir.is_dir():
        raise SystemExit("Invalid path. Please provide a valid directory.")

    output_dir = Path(args.output).resolve() if args.output else audiobook_dir.resolve()
    structure = [s.strip() for s in args.folder_structure.split(',') if s.strip()]

    organize_audiobooks(
        audiobook_dir=audiobook_dir,
        output_dir=output_dir,
        naming=args.naming_convention,
        structure=structure,
        commit=args.commit,
        fetch_metadata=args.fetch_metadata,
        api_key=args.api_key,
        use_cache=not args.no_cache,
        write_tags=args.write_tags,
        enable_benchmark=args.benchmark,
    )


if __name__ == "__main__":
    main()
