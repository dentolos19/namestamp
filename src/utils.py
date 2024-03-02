import random
import string
from pathlib import Path

CHARACTERS = string.ascii_letters + string.digits


def generate_random_string(length: int = 16):
    return "".join(random.choice(CHARACTERS) for _ in range(length))


def check_file_path(path: Path):
    if not path.exists():
        raise FileNotFoundError("The file does not exist.")
    if path.is_dir():
        raise ValueError("The path must be a file, not a directory.")