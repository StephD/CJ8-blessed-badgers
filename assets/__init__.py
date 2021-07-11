from pathlib import Path

path = Path("assets")


def load_asset(filename: str) -> list:
    try:
        with open(path / filename, encoding="utf-8") as f:
            return f.read().splitlines()
    except OSError:
        raise
