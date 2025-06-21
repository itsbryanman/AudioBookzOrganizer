from pathlib import Path

import pytest

from audiobookz_organizer.parser import parse_folder


@pytest.mark.parametrize(
    "foldername, expected_author, expected_title",
    [
        ("Stephen King - The Stand", "Stephen King", "The Stand"),
        ("The Stand - Stephen King", "Stephen King", "The Stand"),
        ("Some Title - Some Author", "Some Author", "Some Title"),
        ("J.R.R. Tolkien - The Hobbit", "J.R.R. Tolkien", "The Hobbit"),
        ("The Girl Who Played with Fire - Stieg Larsson", "Stieg Larsson", "The Girl Who Played with Fire"),
    ],
)
def test_parse_folder_success(foldername, expected_author, expected_title):
    path = Path(foldername)
    audiobook = parse_folder(path)
    assert audiobook is not None
    assert audiobook.author == expected_author
    assert audiobook.title == expected_title


def test_parse_folder_failure():
    audiobook = parse_folder(Path("JustATitle"))
    assert audiobook is None
