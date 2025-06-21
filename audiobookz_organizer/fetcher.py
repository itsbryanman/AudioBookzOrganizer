from __future__ import annotations

import requests


def fetch_book_details(title: str, author: str) -> dict | None:
    """Retrieve metadata from the Google Books API for the given book."""
    params = {"q": f"intitle:{title}+inauthor:{author}"}
    try:
        response = requests.get("https://www.googleapis.com/books/v1/volumes", params=params, timeout=10)
    except requests.RequestException:
        return None
    if response.status_code != 200:
        return None

    data = response.json()
    if data.get("totalItems", 0) == 0:
        return None
    info = data["items"][0]["volumeInfo"]
    return {
        "genre": info.get("categories", ["Unknown Genre"])[0],
        "year": info.get("publishedDate", "0000").split("-")[0],
    }
