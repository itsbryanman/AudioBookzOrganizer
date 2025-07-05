from __future__ import annotations

from pathlib import Path
from typing import Optional
import re

import mutagen

SUPPORTED_EXTENSIONS = {".mp3", ".m4a", ".m4b", ".flac"}


def extract_metadata_from_folder(path: Path) -> Optional[dict[str, str]]:
    """Extract author and title metadata from audio files in ``path``."""
    author = None
    title = None
    genre = None
    year = None
    is_multipart = False

    audio_files = []
    subdirs = []
    
    for item in path.iterdir():
        if item.is_file() and item.suffix.lower() in SUPPORTED_EXTENSIONS:
            audio_files.append(item)
        elif item.is_dir():
            subdirs.append(item)
    
    # Check for multi-part audiobook indicators
    is_multipart = _is_multipart_audiobook(path, audio_files, subdirs)
    
    # Try to extract metadata from audio files
    for file_path in audio_files:
        try:
            audio = mutagen.File(file_path, easy=True)
            if audio:
                current_author = audio.get("artist", [None])[0] or audio.get("albumartist", [None])[0]
                current_title = audio.get("album", [None])[0]
                current_genre = audio.get("genre", [None])[0]
                current_year = audio.get("date", [None])[0]
                
                if current_author and current_title:
                    author = current_author.strip()
                    title = current_title.strip()
                    if current_genre:
                        genre = current_genre.strip()
                    if current_year:
                        year = current_year.strip()[:4]  # Extract year from date
                    
                    result = {"author": author, "title": title, "is_multipart": is_multipart}
                    if genre:
                        result["genre"] = genre
                    if year:
                        result["year"] = year
                    return result
        except mutagen.MutagenError:
            continue
    
    # If no metadata found in audio files, try subdirectories for multi-part books
    if subdirs:
        for subdir in subdirs:
            sub_metadata = extract_metadata_from_folder(subdir)
            if sub_metadata:
                sub_metadata["is_multipart"] = True
                return sub_metadata
    
    return None


def _is_multipart_audiobook(path: Path, audio_files: list[Path], subdirs: list[Path]) -> bool:
    """Determine if this is a multi-part audiobook."""
    # Check for multiple audio files (likely chapters)
    if len(audio_files) > 1:
        return True
    
    # Check for disc/part subdirectories
    disc_pattern = re.compile(r'(disc|disk|part|cd|volume|vol)\s*\d+', re.IGNORECASE)
    for subdir in subdirs:
        if disc_pattern.search(subdir.name):
            return True
    
    # Check for numeric subdirectories that might be parts
    numeric_dirs = [d for d in subdirs if d.name.isdigit()]
    if len(numeric_dirs) > 1:
        return True
    
    return False


def infer_genre_from_text(title: str, author: str, description: str = "") -> str:
    """Infer genre from title, author, or description text."""
    text = f"{title} {author} {description}".lower()
    
    # Genre keywords mapping
    genre_keywords = {
        "Sci-Fi": ["science fiction", "sci-fi", "space", "alien", "future", "robot", "cyberpunk", "dystopian"],
        "Fantasy": ["fantasy", "magic", "wizard", "dragon", "sword", "medieval", "quest", "epic"],
        "Mystery": ["mystery", "detective", "murder", "crime", "investigation", "thriller", "suspense"],
        "Romance": ["romance", "love", "relationship", "heart", "passion", "dating"],
        "Horror": ["horror", "zombie", "vampire", "ghost", "supernatural", "scary", "terror"],
        "Biography": ["biography", "memoir", "life story", "autobiography", "real life"],
        "History": ["history", "historical", "war", "ancient", "century", "empire"],
        "Business": ["business", "entrepreneur", "money", "finance", "leadership", "marketing"],
        "Self-Help": ["self-help", "motivation", "success", "improvement", "guide", "how to"],
        "Young Adult": ["young adult", "ya", "teen", "teenager", "high school", "coming of age"],
        "Literary Fiction": ["literary", "fiction", "novel", "story", "contemporary"],
        "Non-Fiction": ["non-fiction", "facts", "true", "real", "research", "study"],
    }
    
    # Count matches for each genre
    genre_scores = {}
    for genre, keywords in genre_keywords.items():
        score = sum(1 for keyword in keywords if keyword in text)
        if score > 0:
            genre_scores[genre] = score
    
    # Return the genre with the highest score
    if genre_scores:
        return max(genre_scores, key=genre_scores.get)
    
    return "Unknown Genre"
