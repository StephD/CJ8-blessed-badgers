import sys

import blessed

from modules.logger import log
from screens import AboutScreen, GameScreen, LanguageScreen, MenuScreen


def main() -> None:
    """Main function"""
    log("The game start")
    term = blessed.Terminal()
    # Start the menu
    keypressed = None
    # Get the result of the menu to start or the tutorial or game

    with term.fullscreen(), term.cbreak():
        while keypressed != "q":
            keypressed = MenuScreen().render(term)
            if keypressed == "n":  # New game
                print(term.clear)
                GameScreen().render(term)
                pass
            elif keypressed == "t":  # Run the tutorial
                GameScreen("tuto").render(term)
                pass
            elif keypressed == "c":  # Load last game
                # Load the saved game data
                pass
            elif keypressed == "a":  # About the team, jam, why this
                AboutScreen().render(term)
            elif keypressed == "l":  # language selection
                LanguageScreen().render(term)

    log("The game end")
    print(term.clear)
    sys.exit(0)


if __name__ == "__main__":
    main()
