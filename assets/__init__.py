from pathlib import Path

path = Path("assets")


def load_asset(filename: str) -> list[str]:
    """
    Load an asset from the assets/ directory.

    :param filename: name of the file to be loaded
    :return:  a list representing the lines of the asset
    """
    with open(path / filename, encoding="utf-8") as file:
        return file.read().splitlines()
