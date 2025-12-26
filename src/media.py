from datetime import datetime, timezone
from pathlib import Path

from PIL import Image
from win32com.propsys import propsys, pscon  # type: ignore

from patterns import Pattern

VIDEO_EXTENSIONS: list[str] = [".mp4", ".mov", ".avi", ".mkv", ".wmv", ".flv", ".webm"]
NAMING_PATTERNS: list[Pattern] = []
# NAMING_PATTERNS: list[Pattern] = [ScreenshotsPattern(), WhatsAppPattern()]


def get_earliest_date(path: Path):
    date_created = datetime.fromtimestamp(path.stat().st_birthtime)
    date_modified = datetime.fromtimestamp(path.stat().st_mtime)
    return date_created if date_created.timestamp() < date_modified.timestamp() else date_modified


def get_picture_date(path: Path):
    try:
        exif = Image.open(path).getexif()
        if not exif:
            date_taken = None
        date_taken = datetime.strptime(exif[36867], "%Y:%m:%d %H:%M:%S")
    except Exception:
        date_taken = None
    if date_taken:
        return date_taken
    else:
        return get_earliest_date(path)


def get_video_date(path: Path):
    try:
        properties = propsys.SHGetPropertyStoreFromParsingName(str(path))
        media_date = properties.GetValue(pscon.PKEY_Media_DateEncoded).GetValue()
        if not isinstance(media_date, datetime):
            media_date = datetime.fromtimestamp(int(media_date))
            media_date = media_date.replace(tzinfo=timezone.utc)
        return media_date.astimezone()
    except Exception:
        return get_picture_date(path)


def get_media_date(path: Path):
    for pattern in NAMING_PATTERNS:
        if pattern.check_pattern(path):
            return pattern.get_date(path)
    if path.suffix in VIDEO_EXTENSIONS:
        return get_video_date(path)
    return get_picture_date(path)
