from argparse import ArgumentParser
from pathlib import Path

from colorama import Fore, just_fix_windows_console
from engine import rename_items


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

    if len(files) > 0:
        rename_items(
            [Path(item) for item in files],
            force=force,
            recurse=recurse,
            skip_patterns=skip_patterns,
            test=test,
        )
    else:
        input("Please provide at least one file or directory.")
        quit()

    if test:
        print()
        input(f"Press {Fore.CYAN}[Enter]{Fore.RESET} to exit...")
        quit()


if __name__ == "__main__":
    init()