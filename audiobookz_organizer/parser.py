"""Utilities for parsing audiobook folder names."""

from __future__ import annotations

import re
from pathlib import Path

from .models import Audiobook

_PATTERN_AUTHOR_TITLE = re.compile(r"(?P<author>[^-]+) - (?P<title>.+)")
_PATTERN_TITLE_AUTHOR = re.compile(r"(?P<title>.+) - (?P<author>[^-]+)")

FOLDERNAME_PATTERNS = [_PATTERN_AUTHOR_TITLE, _PATTERN_TITLE_AUTHOR]


def _match_pattern(pattern: re.Pattern[str], path: Path) -> Audiobook | None:
    """Return an audiobook if ``path.name`` matches ``pattern``."""
    match = pattern.match(path.name)
    if not match:
        return None
    data = match.groupdict()
    return Audiobook(
        source_path=path,
        author=data.get("author", "Unknown Author").strip(),
        title=data.get("title", "Unknown Title").strip(),
    )


def parse_folder(path: Path) -> Audiobook | None:
    """Parse a folder path into an :class:`Audiobook` instance.

    Parameters
    ----------
    path: Path
        Folder path to parse.

    Returns
    -------
    Audiobook | None
        Parsed audiobook or ``None`` if the folder name does not match known patterns.
    """
    # Heuristic: prefer "title - author" when the author candidate does not
    # start with a leading article such as "the", "a", or "an".
    candidate = _match_pattern(_PATTERN_TITLE_AUTHOR, path)
    if candidate and not candidate.author.lower().startswith(("the ", "a ", "an ")):
        return candidate

    candidate = _match_pattern(_PATTERN_AUTHOR_TITLE, path)
    return candidate
