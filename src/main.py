import argparse
import os
import re
import string
from pathlib import Path

from colorama import Fore

import parsing
import shared

GENERATIVE_CHARACTERS = string.ascii_letters + string.digits
NAMING_PATTERN = r"\d{8}-\d{6}_[a-zA-Z0-9]{4}"


def validate_name(string):
    return re.match(NAMING_PATTERN, string)


def rename_files(files, force=False, indent=0):
    count = 0
    for file in files:
        count += 1
        file_path = Path(file)
        print(f"{' '*indent}[{Fore.BLUE}#{count}{Fore.RESET}] ", end="")
        if file_path.is_dir():
            print(
                f"{Fore.YELLOW}{file_path.name}{Fore.RESET} is a directory, iterating..."
            )
            rename_files(file_path.glob("*"), force, indent + 2)
        else:
            file_directory_path = file_path.parent
            file_extension = file_path.suffix.lower()
            if (not force) and validate_name(file_path.stem):
                print(f"{Fore.GREEN}{file_path.name}{Fore.RESET}")
            else:
                file_time = parsing.get_picture_taken(file_path)
                if file_extension in parsing.VIDEO_EXTENSIONS:
                    file_time = parsing.get_video_taken(file_path)
                new_file_name = f"{file_time.strftime('%Y%m%d-%H%M%S')}_{shared.generate_string(4)}{file_extension}"
                print(
                    f"{Fore.YELLOW}{file_path.name}{Fore.RESET} -> {Fore.GREEN}{new_file_name}{Fore.RESET}"
                )
                file_path.rename(file_directory_path / new_file_name)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs="+", help="the full paths of files to rename")
    parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="forces renaming of files without validation",
    )
    args = parser.parse_args()
    if (args.files is None) or (len(args.files) == 0):
        print("No files specified.")
        input()
        return
    rename_files(args.files, args.force is True)
    input()


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    main()