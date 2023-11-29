import os
import random
import re
from argparse import ArgumentParser
from pathlib import Path

from colorama import Fore

import config
import parsing

NAMING_PATTERN = r"\d{8}-\d{6}_[a-zA-Z0-9]{4}"


def generate_string(length=16, characters=config.GENERATIVE_CHARACTERS):
    return "".join(random.choice(characters) for _ in range(length))


def validate_name(string):
    return re.match(NAMING_PATTERN, string)


def rename_files(files, recurse=False, force=False, indent=0):
    count = 0
    for file in files:
        count += 1
        file_path = Path(file)
        print(f"{' '*indent}[{Fore.BLUE}#{count}{Fore.RESET}] ", end="")
        if file_path.is_dir():
            print(f"{Fore.YELLOW}{file_path.name}{Fore.RESET} is a directory", end="")
            if recurse:
                print(", iterating...")
                rename_files(
                    file_path.glob("*"), True, force, indent + config.INDENT_SIZE
                )
            else:
                print(", skipping...")
                continue
        else:
            file_directory_path = file_path.parent
            file_extension = file_path.suffix.lower()
            if (not force) and validate_name(file_path.stem):
                print(f"{Fore.GREEN}{file_path.name}{Fore.RESET}")
            else:
                file_time = parsing.get_image_taken(file_path)
                new_file_name = f"{file_time.strftime('%Y%m%d-%H%M%S')}_{generate_string(4)}{file_extension}"
                print(
                    f"{Fore.YELLOW}{file_path.name}{Fore.RESET} -> {Fore.GREEN}{new_file_name}{Fore.RESET}"
                )
                file_path.rename(file_directory_path / new_file_name)


def main():
    parser = ArgumentParser()
    parser.add_argument("files", nargs="+", help="the full paths of files to rename")
    parser.add_argument(
        "-r",
        "--recurse",
        action="store_true",
        help="recursively rename files in subdirectories",
    )
    parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="forces renaming of files without validation",
    )
    args = parser.parse_args()
    rename_files(args.files, args.recurse is True, args.force is True)
    print()
    input("Press any key to exit...")
    exit()


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    main()