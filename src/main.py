import re
from argparse import ArgumentParser
from pathlib import Path

from colorama import Fore, just_fix_windows_console
from media import get_media_date
from utils import check_file_path, generate_random_string

INDENT_SIZE = 2
NAMING_PATTERN = r"\d{8}-\d{6}_[a-zA-Z0-9]{4}"


def init():
    parser = ArgumentParser()
    parser.add_argument("files", nargs="*")
    parser.add_argument("-r", "--recurse", action="store_true")
    parser.add_argument("-f", "--force", action="store_true")
    parser.add_argument("-p", "--skip-patterns", action="store_true")
    parser.add_argument("-t", "--test", action="store_true")
    args = parser.parse_args()
    main(
        args.files,
        recurse=args.recurse,
        force=args.force,
        skip_patterns=args.skip_patterns,
        test=args.test,
    )


def main(
    files: list[str],
    recurse: bool,
    force: bool,
    skip_patterns: bool,
    test: bool,
):
    just_fix_windows_console()

    rename_items(
        [Path(item) for item in files],
        force=force,
        recurse=recurse,
        skip_patterns=skip_patterns,
        test=test,
    )

    if test:
        print()
        input(f"Press {Fore.CYAN}[Enter]{Fore.RESET} to exit...")
        quit()


def check_name(value: str):
    return re.match(NAMING_PATTERN, value)


def rename_item(
    path: Path, force: bool = False, skip_patterns: bool = False, test: bool = False
):
    check_file_path(path)
    new_name: str = None
    if not force and check_name(path.stem):
        new_name = path.name
    else:
        time = get_media_date(path, skip_patterns)
        new_name = f"{time.strftime('%Y%m%d-%H%M%S')}_{generate_random_string(4)}{path.suffix.lower()}"
        if not test:
            path.rename(path.with_name(new_name))
    return path.name, new_name


def rename_items(
    paths: list[Path],
    force: bool = False,
    recurse: bool = False,
    skip_patterns: bool = False,
    test: bool = False,
    indent: int = 0,
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
                rename_items(
                    list(path.iterdir()),
                    force,
                    recurse,
                    skip_patterns,
                    test,
                    indent + INDENT_SIZE,
                )
            else:
                print(", skipping...")
        else:
            old_name, new_name = rename_item(path, force, skip_patterns, test)
            if old_name == new_name:
                print(f"{Fore.GREEN}{new_name}{Fore.RESET}")
            else:
                print(
                    f"{Fore.YELLOW}{old_name}{Fore.RESET} -> {Fore.GREEN}{new_name}{Fore.RESET}"
                )


if __name__ == "__main__":
    init()