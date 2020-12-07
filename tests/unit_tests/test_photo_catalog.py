"""Tests for photo_catalog.py module."""

from photo_manage.photo_catalog import Photo
from pathlib import Path
from pytest import mark, raises

test_data = Path('tests/data')


def test_bad_photo_path():
    """Test non-existent file path, expecting exception."""
    with raises(FileNotFoundError):
        Photo(test_data / 'input/not_a_real_file.jpg')


@mark.parametrize('rel_photo_path, original_path_str, original_name, size, new_path_str, new_name',
                  [
                      ('input/20020512.jpg', 'tests/data/input/20020512.jpg',
                       '20020512.jpg', 118726, 'tests/data/input/20020512.jpg', '20020512.jpg'),
                      ('input/20040601.JPG', 'tests/data/input/20040601.JPG',
                       '20040601.JPG', 248573, 'tests/data/input/20040601.JPG', '20040601.JPG'),
                      ('input/subdir/20070701.JPG', 'tests/data/input/subdir/20070701.JPG',
                       '20070701.JPG', 503608, 'tests/data/input/subdir/20070701.JPG', '20070701.JPG'),
                  ])
def test_good_photo_path(rel_photo_path, original_path_str, original_name, size, new_path_str, new_name):
    """Test real photos included in repo tests dir."""
    photo_obj = Photo(test_data / rel_photo_path)
    assert photo_obj.getattr_str('original_path').endswith(original_path_str)
    assert photo_obj.original_name == original_name
    assert photo_obj.size == size
    assert photo_obj.getattr_str('new_path').endswith(new_path_str)
