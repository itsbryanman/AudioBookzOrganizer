from argparse import Namespace

from audiobookz_organizer.cli import parse_args


def test_parse_args_defaults(monkeypatch):
    monkeypatch.setattr(
        'sys.argv',
        ['organize-audiobooks', '--input', '/tmp/in', '--output', '/tmp/out']
    )
    args = parse_args()
    assert isinstance(args, Namespace)
    assert args.input == '/tmp/in'
    assert args.output == '/tmp/out'
    assert args.naming_convention == '{title} - {author}'
    assert args.folder_structure == ''
    assert args.commit is False
    assert args.fetch_metadata is False
