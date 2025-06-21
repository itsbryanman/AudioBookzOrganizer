from __future__ import annotations

from pathlib import Path
from typing import Optional

import mutagen

SUPPORTED_EXTENSIONS = {".mp3", ".m4a", ".m4b", ".flac"}


def extract_metadata_from_folder(path: Path) -> Optional[dict[str, str]]:
    """Extract author and title metadata from audio files in ``path``."""
    author = None
    title = None

    for file_path in path.iterdir():
        if file_path.suffix.lower() in SUPPORTED_EXTENSIONS:
            try:
                audio = mutagen.File(file_path, easy=True)
                if audio:
                    current_author = audio.get("artist", [None])[0]
                    current_title = audio.get("album", [None])[0]
                    if current_author and current_title:
                        author = current_author.strip()
                        title = current_title.strip()
                        return {"author": author, "title": title}
            except mutagen.MutagenError:
                continue
    return None
