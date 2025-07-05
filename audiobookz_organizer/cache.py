"""Metadata caching system for audiobook organization."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Optional, Dict, Any
import hashlib
import time


class MetadataCache:
    """Cache for storing fetched metadata to avoid redundant API calls."""
    
    def __init__(self, cache_dir: Path, cache_type: str = "json"):
        """Initialize the metadata cache.
        
        Parameters
        ----------
        cache_dir: Path
            Directory to store cache files
        cache_type: str
            Type of cache to use ('json' or 'sqlite')
        """
        self.cache_dir = cache_dir
        self.cache_type = cache_type
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        if cache_type == "json":
            self.cache_file = cache_dir / "metadata_cache.json"
            self._cache_data = self._load_json_cache()
        elif cache_type == "sqlite":
            self.cache_file = cache_dir / "metadata_cache.db"
            self._init_sqlite_cache()
        else:
            raise ValueError(f"Unsupported cache type: {cache_type}")
    
    def _generate_key(self, title: str, author: str) -> str:
        """Generate a cache key for the given title and author."""
        combined = f"{title.lower().strip()}|{author.lower().strip()}"
        return hashlib.md5(combined.encode()).hexdigest()
    
    def _load_json_cache(self) -> Dict[str, Any]:
        """Load the JSON cache file."""
        if self.cache_file.exists():
            try:
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return {}
        return {}
    
    def _save_json_cache(self):
        """Save the JSON cache file."""
        try:
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(self._cache_data, f, indent=2, ensure_ascii=False)
        except IOError:
            pass
    
    def _init_sqlite_cache(self):
        """Initialize SQLite cache database."""
        try:
            conn = sqlite3.connect(self.cache_file)
            conn.execute('''
                CREATE TABLE IF NOT EXISTS metadata_cache (
                    key TEXT PRIMARY KEY,
                    title TEXT,
                    author TEXT,
                    genre TEXT,
                    year TEXT,
                    fetched_at REAL,
                    data TEXT
                )
            ''')
            conn.commit()
            conn.close()
        except sqlite3.Error:
            pass
    
    def get(self, title: str, author: str) -> Optional[Dict[str, Any]]:
        """Get cached metadata for the given title and author."""
        key = self._generate_key(title, author)
        
        if self.cache_type == "json":
            return self._cache_data.get(key)
        elif self.cache_type == "sqlite":
            return self._get_from_sqlite(key)
        
        return None
    
    def _get_from_sqlite(self, key: str) -> Optional[Dict[str, Any]]:
        """Get metadata from SQLite cache."""
        try:
            conn = sqlite3.connect(self.cache_file)
            cursor = conn.cursor()
            cursor.execute(
                'SELECT data FROM metadata_cache WHERE key = ?',
                (key,)
            )
            result = cursor.fetchone()
            conn.close()
            
            if result:
                return json.loads(result[0])
        except (sqlite3.Error, json.JSONDecodeError):
            pass
        
        return None
    
    def set(self, title: str, author: str, metadata: Dict[str, Any]):
        """Cache metadata for the given title and author."""
        key = self._generate_key(title, author)
        
        # Add timestamp
        cache_entry = {
            **metadata,
            'cached_at': time.time(),
            'title': title,
            'author': author
        }
        
        if self.cache_type == "json":
            self._cache_data[key] = cache_entry
            self._save_json_cache()
        elif self.cache_type == "sqlite":
            self._set_in_sqlite(key, title, author, cache_entry)
    
    def _set_in_sqlite(self, key: str, title: str, author: str, metadata: Dict[str, Any]):
        """Set metadata in SQLite cache."""
        try:
            conn = sqlite3.connect(self.cache_file)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO metadata_cache 
                (key, title, author, genre, year, fetched_at, data)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                key,
                title,
                author,
                metadata.get('genre', ''),
                metadata.get('year', ''),
                time.time(),
                json.dumps(metadata)
            ))
            conn.commit()
            conn.close()
        except sqlite3.Error:
            pass
    
    def clear(self):
        """Clear all cached metadata."""
        if self.cache_type == "json":
            self._cache_data.clear()
            self._save_json_cache()
        elif self.cache_type == "sqlite":
            self._clear_sqlite()
    
    def _clear_sqlite(self):
        """Clear SQLite cache."""
        try:
            conn = sqlite3.connect(self.cache_file)
            conn.execute('DELETE FROM metadata_cache')
            conn.commit()
            conn.close()
        except sqlite3.Error:
            pass
    
    def size(self) -> int:
        """Get the number of cached entries."""
        if self.cache_type == "json":
            return len(self._cache_data)
        elif self.cache_type == "sqlite":
            return self._sqlite_size()
        return 0
    
    def _sqlite_size(self) -> int:
        """Get size of SQLite cache."""
        try:
            conn = sqlite3.connect(self.cache_file)
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM metadata_cache')
            result = cursor.fetchone()
            conn.close()
            return result[0] if result else 0
        except sqlite3.Error:
            return 0


def get_default_cache_dir() -> Path:
    """Get the default cache directory."""
    if hasattr(Path, 'home'):
        return Path.home() / '.cache' / 'audiobookz_organizer'
    else:
        return Path('.cache') / 'audiobookz_organizer'