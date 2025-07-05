"""Audio file tagging functionality for audiobook organization."""

from __future__ import annotations

from pathlib import Path
from typing import Dict, Any, List
import mutagen
from mutagen.id3 import ID3, TIT2, TPE1, TALB, TCON, TDRC, TPE2
from mutagen.mp4 import MP4

from .models import Audiobook
from .metadata import SUPPORTED_EXTENSIONS


class AudioTagger:
    """Handles updating audio file metadata tags."""
    
    def __init__(self, audiobook: Audiobook):
        """Initialize the tagger with an audiobook.
        
        Parameters
        ----------
        audiobook: Audiobook
            The audiobook to process
        """
        self.audiobook = audiobook
        self.supported_files = self._get_supported_files()
    
    def _get_supported_files(self) -> List[Path]:
        """Get all supported audio files in the audiobook folder."""
        files = []
        for file_path in self.audiobook.source_path.rglob("*"):
            if file_path.is_file() and file_path.suffix.lower() in SUPPORTED_EXTENSIONS:
                files.append(file_path)
        return files
    
    def update_tags(self, dry_run: bool = False) -> Dict[str, Any]:
        """Update tags for all audio files in the audiobook.
        
        Parameters
        ----------
        dry_run: bool
            If True, only report what would be changed without making changes
            
        Returns
        -------
        Dict[str, Any]
            Statistics about the tagging operation
        """
        stats = {
            "files_processed": 0,
            "files_updated": 0,
            "files_skipped": 0,
            "errors": []
        }
        
        for file_path in self.supported_files:
            try:
                result = self._update_file_tags(file_path, dry_run)
                stats["files_processed"] += 1
                if result:
                    stats["files_updated"] += 1
                else:
                    stats["files_skipped"] += 1
            except Exception as e:
                stats["errors"].append(f"{file_path.name}: {str(e)}")
        
        return stats
    
    def _update_file_tags(self, file_path: Path, dry_run: bool) -> bool:
        """Update tags for a single audio file.
        
        Parameters
        ----------
        file_path: Path
            Path to the audio file
        dry_run: bool
            If True, only report what would be changed
            
        Returns
        -------
        bool
            True if tags were updated, False otherwise
        """
        try:
            audio = mutagen.File(file_path)
            if not audio:
                return False
            
            # Determine file type and update accordingly
            if file_path.suffix.lower() == '.mp3':
                return self._update_mp3_tags(audio, dry_run)
            elif file_path.suffix.lower() in ['.m4a', '.m4b']:
                return self._update_mp4_tags(audio, dry_run)
            elif file_path.suffix.lower() == '.flac':
                return self._update_flac_tags(audio, dry_run)
            
        except mutagen.MutagenError:
            return False
        
        return False
    
    def _update_mp3_tags(self, audio: mutagen.FileType, dry_run: bool) -> bool:
        """Update MP3 ID3 tags."""
        # Add ID3 tags if they don't exist
        if not hasattr(audio, 'tags') or audio.tags is None:
            audio.add_tags()
        
        tags = audio.tags
        updated = False
        
        # Update tags
        tag_mappings = {
            'TIT2': self.audiobook.title,      # Title
            'TPE1': self.audiobook.author,     # Artist
            'TALB': self.audiobook.title,      # Album
            'TPE2': self.audiobook.author,     # Album Artist
            'TCON': self.audiobook.genre,      # Genre
            'TDRC': self.audiobook.year,       # Year
        }
        
        for tag_name, value in tag_mappings.items():
            if value and value != "Unknown":
                current_value = tags.get(tag_name)
                if not current_value or str(current_value) != value:
                    if not dry_run:
                        if tag_name == 'TIT2':
                            tags[tag_name] = TIT2(encoding=3, text=value)
                        elif tag_name == 'TPE1':
                            tags[tag_name] = TPE1(encoding=3, text=value)
                        elif tag_name == 'TALB':
                            tags[tag_name] = TALB(encoding=3, text=value)
                        elif tag_name == 'TPE2':
                            tags[tag_name] = TPE2(encoding=3, text=value)
                        elif tag_name == 'TCON':
                            tags[tag_name] = TCON(encoding=3, text=value)
                        elif tag_name == 'TDRC':
                            tags[tag_name] = TDRC(encoding=3, text=value)
                    updated = True
        
        if updated and not dry_run:
            audio.save()
        
        return updated
    
    def _update_mp4_tags(self, audio: mutagen.FileType, dry_run: bool) -> bool:
        """Update MP4/M4A/M4B tags."""
        if not hasattr(audio, 'tags') or audio.tags is None:
            audio.add_tags()
        
        tags = audio.tags
        updated = False
        
        # MP4 tag mappings
        tag_mappings = {
            '©nam': self.audiobook.title,      # Title
            '©ART': self.audiobook.author,     # Artist
            '©alb': self.audiobook.title,      # Album
            'aART': self.audiobook.author,     # Album Artist
            '©gen': self.audiobook.genre,      # Genre
            '©day': self.audiobook.year,       # Year
        }
        
        for tag_name, value in tag_mappings.items():
            if value and value != "Unknown":
                current_value = tags.get(tag_name)
                if not current_value or str(current_value[0]) != value:
                    if not dry_run:
                        tags[tag_name] = [value]
                    updated = True
        
        if updated and not dry_run:
            audio.save()
        
        return updated
    
    def _update_flac_tags(self, audio: mutagen.FileType, dry_run: bool) -> bool:
        """Update FLAC tags."""
        if not hasattr(audio, 'tags') or audio.tags is None:
            audio.add_tags()
        
        tags = audio.tags
        updated = False
        
        # FLAC tag mappings
        tag_mappings = {
            'TITLE': self.audiobook.title,
            'ARTIST': self.audiobook.author,
            'ALBUM': self.audiobook.title,
            'ALBUMARTIST': self.audiobook.author,
            'GENRE': self.audiobook.genre,
            'DATE': self.audiobook.year,
        }
        
        for tag_name, value in tag_mappings.items():
            if value and value != "Unknown":
                current_value = tags.get(tag_name)
                if not current_value or str(current_value[0]) != value:
                    if not dry_run:
                        tags[tag_name] = [value]
                    updated = True
        
        if updated and not dry_run:
            audio.save()
        
        return updated


def update_audiobook_tags(audiobook: Audiobook, dry_run: bool = False) -> Dict[str, Any]:
    """Update tags for an audiobook.
    
    Parameters
    ----------
    audiobook: Audiobook
        The audiobook to process
    dry_run: bool
        If True, only report what would be changed
        
    Returns
    -------
    Dict[str, Any]
        Statistics about the tagging operation
    """
    tagger = AudioTagger(audiobook)
    return tagger.update_tags(dry_run)