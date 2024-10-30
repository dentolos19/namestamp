from os import path
from zipfile import ZipFile

from main import main


def test():
    if not path.exists("docs/examples"):
        with ZipFile("docs/examples.zip", "r") as zip:
            zip.extractall("docs/examples")
    main(["docs/examples"], test=True)


if __name__ == "__main__":
    test()