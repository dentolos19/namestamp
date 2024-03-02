import re
from datetime import datetime
from pathlib import Path

from utils import check_file_path


class ScreenshotsPattern:
    # example: Screenshot_20240114_110317_Mobile Legends Bang Bang
    NAMING_PATTERN = r"Screenshot_\d{8}_\d{6}_.*"

    def check_pattern(self, path: Path):
        check_file_path(path)
        return re.fullmatch(self.NAMING_PATTERN, path.stem) is not None

    def get_date(self, path: Path):
        check_file_path(path)
        try:
            split = path.stem.split("_")
            time = datetime.strptime(split[1] + split[2], "%Y%m%d%H%M%S")
            return time
        except Exception:
            return None