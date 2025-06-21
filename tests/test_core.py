from pathlib import Path

import pytest

from audiobookz_organizer.core import organize_audiobooks


@pytest.fixture
def mock_library(tmp_path: Path):
    input_dir = tmp_path / "input"
    output_dir = tmp_path / "output"
    input_dir.mkdir()
    output_dir.mkdir()

    (input_dir / "Brandon Sanderson - The Way of Kings").mkdir()
    (input_dir / "Project Hail Mary - Andy Weir").mkdir()
    (input_dir / "Unparseable Folder").mkdir()

    return input_dir, output_dir


def test_organize_audiobooks_dry_run(mock_library, capsys):
    input_dir, output_dir = mock_library
    organize_audiobooks(
        audiobook_dir=input_dir,
        output_dir=output_dir,
        naming="{author} - {title}",
        structure=["author"],
        commit=False,
    )

    captured = capsys.readouterr()
    assert "Would move" in captured.out
    assert len(list(output_dir.iterdir())) == 0
    assert len(list(input_dir.iterdir())) == 3


def test_organize_audiobooks_commit(mock_library):
    input_dir, output_dir = mock_library
    organize_audiobooks(
        audiobook_dir=input_dir,
        output_dir=output_dir,
        naming="{author} - {title}",
        structure=["author"],
        commit=True,
    )

    author_dir = output_dir / "Brandon Sanderson"
    assert author_dir.exists()
    assert (author_dir / "Brandon Sanderson - The Way of Kings").exists()

    author_dir_2 = output_dir / "Andy Weir"
    assert author_dir_2.exists()
    assert (author_dir_2 / "Andy Weir - Project Hail Mary").exists()

    assert not (input_dir / "Brandon Sanderson - The Way of Kings").exists()
