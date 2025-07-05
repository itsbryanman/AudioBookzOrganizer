from pathlib import Path

import mutagen
import pytest

from audiobookcleanr.metadata import extract_metadata_from_folder


class DummyAudio:
    def __init__(self, artist: str | None, album: str | None):
        self.tags = {}
        if artist:
            self.tags['artist'] = [artist]
        if album:
            self.tags['album'] = [album]

    def get(self, key, default=None):
        return self.tags.get(key, default)


@pytest.fixture
def tmp_audio_folder(tmp_path: Path) -> Path:
    folder = tmp_path / "book"
    folder.mkdir()
    (folder / "track.mp3").write_bytes(b'fake')
    return folder


def test_extract_metadata_from_folder(tmp_audio_folder, monkeypatch):
    def dummy_file(path, easy):
        return DummyAudio('Author', 'Title')

    monkeypatch.setattr(mutagen, 'File', dummy_file)
    meta = extract_metadata_from_folder(tmp_audio_folder)
    assert meta == {'author': 'Author', 'title': 'Title'}
