from datetime import datetime
from pathlib import Path

import pytz
import tzlocal
from PIL import Image
from win32com.propsys import propsys, pscon

VIDEO_EXTENSIONS = [".mp4", ".mov", ".avi", ".mkv", ".wmv", ".flv", ".webm"]

def get_image_taken(file_path):
    path = Path(file_path)
    if (path.suffix.lower() in VIDEO_EXTENSIONS):
        return get_video_taken(file_path)
    return get_picture_taken(file_path)

def get_earilest_date(file_path):
    """
    Get the earliest date attribute of a file.
    """
    date_created = datetime.fromtimestamp(file_path.stat().st_ctime)
    date_modified = datetime.fromtimestamp(file_path.stat().st_mtime)
    return (
        date_created
        if date_created.timestamp() < date_modified.timestamp()
        else date_modified
    )

def get_picture_taken(file_path):
    """
    Get the date taken attribute of a picture file.
    Fall backs to the earliest date attribute if date taken is not available.
    """
    try:
        exif = Image.open(file_path)._getexif()
        if not exif:
            date_taken = None
        date_taken = datetime.strptime(exif[36867], "%Y:%m:%d %H:%M:%S")
    except Exception:
        date_taken = None
    if date_taken:
        return date_taken
    else:
        return get_earilest_date(file_path)


def get_video_taken(file_path):
    """
    Gets the media created attribute of a video file.
    Fall backs to the earliest date attribute if media created is not available.
    """
    try:
        p = propsys.SHGetPropertyStoreFromParsingName(str(file_path))
        dt = p.GetValue(pscon.PKEY_Media_DateEncoded).GetValue()
        if not isinstance(dt, datetime):
            dt = datetime.fromtimestamp(int(dt))
            dt = dt.replace(tzinfo=pytz.timezone("UTC"))
        return dt.astimezone(tzlocal.get_localzone())
    except Exception:
        return get_picture_taken(file_path)