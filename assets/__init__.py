
def load_asset(filename: str) -> list:
    try:
        with open(filename) as f:
            return f.read().splitlines()
    except OSError:
        raise
