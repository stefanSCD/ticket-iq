"""Shared integrity rules for loose ToolNest files and optional archive copies."""

import hashlib


OPTIONAL_ARCHIVES = ('toolnest-docs.zip', 'toolnest-tickets.zip')
TEXT_SUFFIXES = {'.md', '.json', '.jsonl', '.csv', '.py'}


def content_hash(data, suffix):
    """Hash text with LF newlines so Windows checkouts retain the same integrity."""
    if suffix in TEXT_SUFFIXES:
        data = data.replace(b'\r\n', b'\n')
    return hashlib.sha256(data).hexdigest()


def file_hash(path):
    return content_hash(path.read_bytes(), path.suffix)
