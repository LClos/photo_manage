"""Tools to discover photos in a given directory."""
import sys

from typing  import Iterator, Union
from pathlib import Path


def find_photos(photos_dir: Union[str, Path]) -> Iterator[Path]:
    """Recursively search input directory for images with known extensions.

    Args:
        photos_dir:

    Yields:
        path of images

    """
    photos_dir = Path(photos_dir)
    for path_in in photos_dir.iterdir():
        if path_in.is_dir():
            for subdir_p in find_photos(path_in):
                yield subdir_p
        if path_in.suffix.lower() in ['.jpeg', '.jpg', '.gif']:
            yield path_in


if __name__ == '__main__':
    photo_dir = sys.argv[1]
    for p in iter(photo for photo in find_photos(photo_dir)):
        print(p.resolve())
