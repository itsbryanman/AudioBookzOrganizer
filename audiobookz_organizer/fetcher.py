from __future__ import annotations

import requests


def fetch_book_details(title: str, author: str, api_key: str | None = None) -> dict | None:
    """Retrieve metadata from the Google Books API for the given book."""
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

    return {
        "genre": categories[0],
        "year": published_date.split("-")[0],
    }
