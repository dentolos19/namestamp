import argparse
import os
import random
import re
import string
from pathlib import Path

from colorama import Fore

GENERATIVE_CHARACTERS = string.ascii_letters + string.digits
NAME_LENGTH = 16
NAME_PATTERN = "[a-zA-Z0-9]" + "{" + str(NAME_LENGTH) + "}"


def generate_random_string():
    return "".join(random.choice(GENERATIVE_CHARACTERS) for _ in range(NAME_LENGTH))


def validate_name(string):
    return re.match(NAME_PATTERN, string)


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
                    new_file_name = generate_random_string() + file_extension
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