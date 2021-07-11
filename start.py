import sys

import blessed

from modules.logger import log
from scenes import StartScene


def main() -> None:
    """Main function"""
    log("The game start")
    term = blessed.Terminal()
    # Start the menu
    keypressed = StartScene().render(term)
    log(keypressed, "keypressed")
    # Get the result of the menu to start or the tutorial or game
    if keypressed != "q":
        if keypressed == "n":  # New game
            log("New game", "menu")
            pass
        elif keypressed == "t":  # Run the tutorial
            log("New tutorial", "menu")
            pass
        elif keypressed == "c":  # Load last game
            log("Load last game", "menu")
            # Load the saved game data
            pass
        elif keypressed == "a":  # About the team, jam, why this
            log("About the game", "menu")
            pass

    log("The game end")
    sys.exit(0)


if __name__ == "__main__":
    main()
