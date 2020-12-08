"""Tools to build and query collection of photo files."""

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path, PosixPath, WindowsPath
from typing import Generic, Iterator, Optional, TypeVar, Union

from photo_manage.photo_discovery import find_photos

T = TypeVar('T')


@dataclass
class Photo:
    """Dataclass to collect and store basic metadata on input photo file input. Removes need for multiple outside calls for file stats (expensive)."""
    original_path: Union[Path, str]
    original_name: Optional[str]      = field(init=False)
    original_date: Optional[datetime] = field(init=False)
    size:          Optional[int]      = field(init=False)
    new_path:      Optional[Path]     = field(init=False)
    _new_path:     Optional[Union[Path, str]] = field(default='', init=False, repr=False)
    new_name:      Optional[str]      = field(init=False)

    def __post_init__(self):
        """Post initialization setting of data class attributes.  New path and name default to original."""
        self.original_path = Path(self.original_path)
        self.original_name = self.original_path.name
        filestats          = self.original_path.stat()
        self.original_date = min(datetime.fromtimestamp(filestats.st_ctime),
                                 datetime.fromtimestamp(filestats.st_mtime))
        self.size          = filestats.st_size
        self.new_path      = self.original_path
        return

    @property
    def new_path(self) -> Path:
        """Make <Photo instance>.new_path attribute calls pull from hidden attribute."""
        return self._new_path

    @new_path.setter
    def new_path(self, path: Path) -> None:
        """Make setting of <Photo instance>.new_path attribute set hidden attribute and set derived new_name attribute."""
        if type(path) is property:
            path = Photo._new_path
        self._new_path = Path(path)
        self.new_name  = self._new_path.name

    def getattr_str(self, attr: str) -> str:
        """Convenience function to return human-readable string representation of attribute."""
        value = self.__getattribute__(attr)
        value_type = type(value)
        if value_type == datetime:
            value = value.strftime(T.date_format)
        elif value_type in [PosixPath, WindowsPath]:
            value = value.resolve().as_posix()
        return value


Photo.date_format = '%Y%m%d_%H:%M:%S'  # type: str


class PhotoCollection(Generic[T]):
    def __init__(self, input_photos_dir):
        self.source_dir = Path(input_photos_dir)
        self.photos     = [Photo(photo) for photo in find_photos(self.source_dir)]

    def __iter__(self) -> Iterator[T]:
        return iter(self.photos)

    def get_photo_table(self, delimiter: str = '\t') -> Iterator[str]:
        headers = ['original_path', 'original_name', 'original_date', 'size', 'new_path', 'new_name']
        yield f'{delimiter.join(headers)}'
        compare = self.photos[0]
        for photo in self.photos:
            yield f'{delimiter.join([str(photo.getattr_str(h)) for h in headers])}'

    # def write_photos(self, output_photos_dir: Union[str, Path]):


def build_photo_collection(input_photos_dir, output_photos_dir):
    source_collection = PhotoCollection(input_photos_dir)
    return source_collection


if __name__ == '__main__':

    srcdir = Path.cwd()
    input_dir = srcdir / '../tests/data/input'
    output_dir = srcdir / '../tests/data/output'
    test = build_photo_collection(input_dir, output_dir)
    for line in test.get_photo_table():
        print(f'{line}')

    # photo_dir = sys.argv[1]
    # photos = [Photo(original_path=photo,
    #                 new_name='newname.jpg')
    #           for photo in find_photos(photo_dir)]
    # for p in photos:
    #     print(p)
