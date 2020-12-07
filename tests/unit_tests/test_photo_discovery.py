"""Tests for photo_catalog.py module."""

from photo_manage.photo_discovery import find_photos
from pathlib import Path
from pytest import mark, raises

test_data = Path('tests/data')

@mark.parametrize('rel_photo_path, expected_result',
                  [
                      (),
                      (),
                      ()
                  ])
def test_find_photos():
