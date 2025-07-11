"""Data models for audiobook organization."""

from dataclasses import dataclass
from pathlib import Path

from .utils import sanitize_filename

@dataclass
class Audiobook:
    """Representation of an audiobook folder."""

    source_path: Path
    author: str = "Unknown Author"
    title: str = "Unknown Title"
    genre: str = "Unknown Genre"
    year: str = "0000"
    is_multipart: bool = False

    def get_target_path(self, base_dir: Path, naming_convention: str, structure: list[str]) -> Path:
        """Construct destination path for this audiobook.

        Parameters
        ----------
        base_dir: Path
            Root directory where organized audiobooks are placed.
        naming_convention: str
            Pattern for the final folder name; placeholders ``{author}``, ``{title}``, ``{genre}``, and ``{year}`` are allowed.
        structure: list[str]
            Sequence of fields used as subdirectories (e.g., ``["genre", "author"]``).

        Returns
        -------
        Path
            The full target path where the audiobook should be moved.
        """
        parts: list[str] = []
        for field in structure:
            value = getattr(self, field, f"Unknown {field.title()}").strip()
            parts.append(sanitize_filename(value))

        target_base = base_dir.joinpath(*parts)
        clean_author = sanitize_filename(self.author)
        clean_title = sanitize_filename(self.title)
        clean_genre = sanitize_filename(self.genre)
        clean_year = sanitize_filename(self.year)
        
        folder_name = naming_convention.format(
            author=clean_author, 
            title=clean_title, 
            genre=clean_genre, 
            year=clean_year
        )
        return target_base / folder_name
