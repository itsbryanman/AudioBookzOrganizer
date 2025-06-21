"""Data models for audiobook organization."""

from dataclasses import dataclass
from pathlib import Path

@dataclass
class Audiobook:
    """Representation of an audiobook folder."""

    source_path: Path
    author: str = "Unknown Author"
    title: str = "Unknown Title"

    def get_target_path(self, base_dir: Path, naming_convention: str, structure: list[str]) -> Path:
        """Construct destination path for this audiobook.

        Parameters
        ----------
        base_dir: Path
            Root directory where organized audiobooks are placed.
        naming_convention: str
            Pattern for the final folder name; placeholders ``{author}`` and ``{title}`` are allowed.
        structure: list[str]
            Sequence of fields used as subdirectories (e.g., ``["author"]``).

        Returns
        -------
        Path
            The full target path where the audiobook should be moved.
        """
        parts: list[str] = []
        for field in structure:
            value = getattr(self, field, f"Unknown {field.title()}").strip()
            parts.append(value)
        target_base = base_dir.joinpath(*parts)
        folder_name = naming_convention.format(author=self.author, title=self.title)
        return target_base / folder_name
