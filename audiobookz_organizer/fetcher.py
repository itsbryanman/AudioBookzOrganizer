from __future__ import annotations

import requests
from pathlib import Path
from typing import Optional

from .cache import MetadataCache, get_default_cache_dir


def fetch_book_details(
    title: str, 
    author: str, 
    api_key: str | None = None,
    use_cache: bool = True,
    cache_dir: Optional[Path] = None
) -> dict | None:
    """Retrieve metadata from the Google Books API for the given book.
    
    Parameters
    ----------
    title: str
        Book title to search for
    author: str
        Book author to search for
    api_key: str | None
        Google Books API key for higher quotas
    use_cache: bool
        Whether to use cached results
    cache_dir: Path | None
        Directory to store cache files
    
    Returns
    -------
    dict | None
        Metadata dictionary or None if not found
    """
    if not title or not author:
        return None
    
    # Initialize cache if enabled
    cache = None
    if use_cache:
        cache_path = cache_dir or get_default_cache_dir()
        cache = MetadataCache(cache_path, cache_type="json")
        
        # Check cache first
        cached_result = cache.get(title, author)
        if cached_result:
            return {
                "genre": cached_result.get("genre", "Unknown Genre"),
                "year": cached_result.get("year", "0000"),
            }
    
    # Fetch from API
    params = {"q": f"intitle:{title}+inauthor:{author}"}
    if api_key:
        params["key"] = api_key
    
    try:
        response = requests.get("https://www.googleapis.com/books/v1/volumes", params=params, timeout=10)
    except requests.RequestException:
        return None
    
    if response.status_code != 200:
        return None

    data = response.json()
    if data.get("totalItems", 0) == 0:
        return None

    items = data.get("items")
    if not items:
        return None

    volume_info = items[0].get("volumeInfo", {})
    if not volume_info:
        return None

    categories = volume_info.get("categories", ["Unknown Genre"])
    published_date = volume_info.get("publishedDate", "0000")

    result = {
        "genre": categories[0],
        "year": published_date.split("-")[0],
    }
    
    # Cache the result
    if cache:
        cache.set(title, author, result)
    
    return result
