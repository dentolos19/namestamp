from argparse import ArgumentParser
from pathlib import Path

from colorama import Fore

from engine import get_items


def init():
    parser = ArgumentParser()
    parser.add_argument("files", nargs="*")
    args = parser.parse_args()
    main(args.files)


def main(files: list[str], test: bool = False):
    items = get_items([Path(file) for file in files])
    for index, item in enumerate(items):
        print(f"[{Fore.BLUE}#{index + 1}{Fore.RESET}] ", end="")
        print(
            f"{Fore.YELLOW}{item.name}{Fore.RESET} -> {Fore.GREEN}{item.new_name}{Fore.RESET}"
        )
        if not test:
            item.rename()

    input()


if __name__ == "__main__":
    init()