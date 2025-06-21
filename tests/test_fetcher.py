from unittest.mock import Mock

import requests

from audiobookz_organizer.fetcher import fetch_book_details


def test_fetch_book_details_success(mocker):
    mock_resp = Mock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {
        'totalItems': 1,
        'items': [{
            'volumeInfo': {
                'categories': ['Fiction'],
                'publishedDate': '2001-01-01'
            }
        }]
    }
    mocker.patch.object(requests, 'get', return_value=mock_resp)

    info = fetch_book_details('Title', 'Author')
    assert info == {'genre': 'Fiction', 'year': '2001'}
