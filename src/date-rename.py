import argparse
import os
import re
import string
from datetime import datetime
from pathlib import Path

from colorama import Fore
from PIL import Image

import shared

GENERATIVE_CHARACTERS = string.ascii_letters + string.digits
NAMING_PATTERN = r"\d{8}-\d{6}_[a-zA-Z0-9]{4}"


def validate_name(string):
    return re.match(NAMING_PATTERN, string)


def get_file_date(file_path):
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


def rename_files(files, indent=0):
    count = 0
    for file in files:
        count += 1
        file_path = Path(file)
        print(f"{' '*indent}[{Fore.BLUE}#{count}{Fore.RESET}] ", end="")
        try:
            if file_path.is_dir():
                print(
                    f"{Fore.YELLOW}{file_path.name}{Fore.RESET} is a directory, iterating..."
                )
                rename_files(file_path.glob("*"), indent + 2)
            else:
                file_directory_path = file_path.parent
                file_extension = file_path.suffix.lower()
                if validate_name(file_path.stem):
                    print(f"{Fore.GREEN}{file_path.name}{Fore.RESET}")
                else:
                    file_time = get_file_date(file_path)
                    new_file_name = f"{file_time.strftime('%Y%m%d-%H%M%S')}_{shared.generate_string(4)}{file_extension}"
                    print(
                        f"{Fore.YELLOW}{file_path.name}{Fore.RESET} -> {Fore.GREEN}{new_file_name}{Fore.RESET}"
                    )
                    file_path.rename(file_directory_path / new_file_name)
        except Exception as exception:
            print(f"{Fore.RED}{exception}{Fore.RESET}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs="+")
    args = parser.parse_args()
    if (args.files is None) or (len(args.files) == 0):
        print("No files specified.")
        return
    rename_files(args.files)
    input()


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    main()