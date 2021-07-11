import sys

import blessed

from scenes import StartScene


def main() -> None:
    """Main function"""
    print("Hello Blessed Badgers !!")
    term = blessed.Terminal()
    StartScene().render(term)

    # Start the menu
    # Get the result of the menu to start or the tutorial or game

    sys.exit(0)


if __name__ == "__main__":
    main()
