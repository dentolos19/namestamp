import random
import string
from datetime import datetime
from pathlib import Path

import pywintypes
import win32file


def generate_random_string(
    length: int = 16, characters: str = string.ascii_letters + string.digits
):
    return "".join(random.choice(characters) for _ in range(length))


def modify_file_creation_time(path: Path, time: datetime):
    handle = win32file.CreateFile(
        str(path), win32file.GENERIC_WRITE, 0, None, win32file.OPEN_EXISTING, 0, 0
    )
    time = pywintypes.Time(int(time.timestamp()))
    win32file.SetFileTime(handle, time)