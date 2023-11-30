import re
from argparse import ArgumentParser
from pathlib import Path

from colorama import Fore

from media import get_media_date
from utils import generate_string

NAMING_PATTERN = r"\d{8}-\d{6}_[a-zA-Z0-9]{4}"


def main():
    parser = ArgumentParser()
    parser.add_argument("files", nargs="*")
    parser.add_argument("-r", "--recurse", action="store_true")
    parser.add_argument("-f", "--force", action="store_true")
    args = parser.parse_args()
    rename_items([Path(item) for item in args.files], args.force, args.recurse)
    print()
    input("Press [Enter] to exit...")
    quit()


import re


def check_name(value: str):
    """
    Check if the given value matches the naming pattern.
    """
    return re.match(NAMING_PATTERN, value)


def rename_item(path: Path, force: bool = False):
    if path.is_dir():
        raise ValueError("The path must be a file, not a directory.")
    new_name: str = None
    if not force and check_name(path.stem):
        new_name = path.name
    else:
        time = get_media_date(path)
        new_name = f"{time.strftime('%Y%m%d-%H%M%S')}_{generate_string(4)}{path.suffix.lower()}"
        path.rename(path.with_name(new_name))
    return path.name, new_name


def rename_items(
    paths: list[Path], force: bool = False, recurse: bool = False, indent: int = 0
):
    if len(paths) == 1 and paths[0].is_dir():
        paths = list(paths[0].iterdir())
    for index, path in enumerate(paths):
        print(" " * indent, end="")
        print(f"[{Fore.BLUE}#{index + 1}{Fore.RESET}] ", end="")
        if path.is_dir():
            print(f"{Fore.YELLOW}{path.name}{Fore.RESET} is a directory", end="")
            if recurse:
                print(", recursing...")
                rename_items(list(path.iterdir()), force, recurse, indent + 2)
            else:
                print(", skipping...")
        else:
            old_name, new_name = rename_item(path, force)
            if old_name == new_name:
                print(f"{Fore.GREEN}{new_name}{Fore.RESET}")
            else:
                print(
                    f"{Fore.YELLOW}{old_name}{Fore.RESET} -> {Fore.GREEN}{new_name}{Fore.RESET}"
                )


if __name__ == "__main__":
    main()