from __future__ import annotations

import re

_illegal_pattern = re.compile(r'[<>:"/\\|?*]')


def sanitize_filename(name: str) -> str:
    """Return ``name`` with illegal filesystem characters removed."""
    return _illegal_pattern.sub('', name)
