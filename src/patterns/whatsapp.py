import re
from datetime import datetime
from pathlib import Path

from utils import check_file_path, modify_file_creation_time


class WhatsAppPattern:
    # example: IMG-20210531-WA0000, VID-20210531-WA0000
    NAMING_PATTERN = r"(IMG|VID)-\d{8}-WA\d{4}"

    def check_pattern(self, path: Path):
        check_file_path(path)
        return re.fullmatch(self.NAMING_PATTERN, path.stem) is not None

    def get_date(self, path: Path):
        check_file_path(path)
        try:
            time = datetime.strptime(path.name.split("-")[1], "%Y%m%d")
            modify_file_creation_time(path, time)
            return time
        except Exception:
            return None