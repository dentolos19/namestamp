import re
from pathlib import Path

from media import get_media_date
from utils import generate_random_string

NAMING_PATTERN = r"\d{8}-\d{6}_[a-zA-Z0-9]{4}"


class Item:
    def __init__(self, path: Path):
        self.path = path
        self.name = path.name
        self.new_name = path.name

        if not re.fullmatch(NAMING_PATTERN, path.stem):
            time = get_media_date(path)
            self.new_name = f"{time.strftime('%Y%m%d-%H%M%S')}_{generate_random_string(4)}{path.suffix.lower()}"

    def rename(self):
        if self.name == self.new_name:
            return False
        self.path = self.path.rename(self.path.with_name(self.new_name))
        self.name = self.path.name
        return True


def get_items(paths: list[Path]):
    items: list[Item] = []
    for path in paths:
        items.extend(get_item(path))
    return items


def get_item(path: Path):
    items: list[Item] = []
    if path.is_file():
        items.append(Item(path))
    else:
        for item in path.iterdir():
            items.extend(get_item(item))
    return items