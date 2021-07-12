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
    log(keypressed, "keypressed")
    # Get the result of the menu to start or the tutorial or game

    with term.fullscreen(), term.cbreak():
        while keypressed != "q":
            keypressed = MenuScreen().render(term)
            if keypressed == "n":  # New game
                log("New game", "menu")
                GameScreen().render(term)
                pass
            elif keypressed == "t":  # Run the tutorial
                log("New tutorial", "menu")
                GameScreen("tuto").render(term)
                pass
            elif keypressed == "c":  # Load last game
                log("Load last game", "menu")
                # Load the saved game data
                pass
            elif keypressed == "a":  # About the team, jam, why this
                log("About the game", "menu")
                AboutScreen().render(term)
            elif keypressed == "l":  # language selection
                log("Language selector opened")
                LanguageScreen().render(term)

    log("The game end")
    print(term.clear)
    sys.exit(0)


if __name__ == "__main__":
    main()
