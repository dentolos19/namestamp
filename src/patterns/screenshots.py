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
            split_stem = path.stem.split("_")
            return datetime.strptime(split_stem[1] + split_stem[2], "%Y%m%d%H%M%S")
        except Exception:
            return None