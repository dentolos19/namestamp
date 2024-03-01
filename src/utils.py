import random
import string
from datetime import datetime
from pathlib import Path

import pywintypes
import win32file

CHARACTERS = string.ascii_letters + string.digits


def generate_random_string(length: int = 16):
    return "".join(random.choice(CHARACTERS) for _ in range(length))


def check_file_path(path: Path):
    if not path.exists():
        raise FileNotFoundError("The file does not exist.")
    if path.is_dir():
        raise ValueError("The path must be a file, not a directory.")


def modify_file_creation_time(path: Path, time: datetime):
    handle = win32file.CreateFile(
        str(path), win32file.GENERIC_WRITE, 0, None, win32file.OPEN_EXISTING, 0, 0
    )
    time = pywintypes.Time(int(time.timestamp()))
    win32file.SetFileTime(handle, time)