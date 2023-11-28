from datetime import datetime

import pytz
from PIL import Image
from win32com.propsys import propsys, pscon

VIDEO_EXTENSIONS = [".mp4", ".mov", ".avi", ".mkv", ".wmv", ".flv", ".webm"]

def get_picture_taken(file_path):
    """
    Get the date taken attribute of a picture file.
    Fall backs to the date modified or date created attribute if date taken is not available.
    """
    date_created = datetime.fromtimestamp(file_path.stat().st_ctime)
    date_modified = datetime.fromtimestamp(file_path.stat().st_mtime)
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
        return (
            date_created
            if date_created.timestamp() < date_modified.timestamp()
            else date_modified
        )


def get_video_taken(file_path):
    """
    Gets the media created attribute of a video file.
    Fall backs to the date modified or date created attribute if date taken is not available.
    """
    try:
        properties = propsys.SHGetPropertyStoreFromParsingName(str(file_path))
        dt = properties.GetValue(pscon.PKEY_Media_DateEncoded).GetValue()
        if not isinstance(dt, datetime):
            dt = datetime.fromtimestamp(int(dt))
            dt = dt.replace(tzinfo=pytz.timezone("UTC"))
        return dt.astimezone(pytz.timezone("Asia/Singapore"))
    except Exception:
        return get_picture_taken(file_path)