import sys

import blessed

from modules.game_data import GameData
from modules.logger import log
from screens import AboutScreen, GameScreen, LanguageScreen, MenuScreen


def main() -> None:
    """Main function"""
    log("The game start", "Title")
    term = blessed.Terminal()
    game_data = GameData()
    keypressed = None

    with term.fullscreen(), term.cbreak():
        while keypressed != "q":
            keypressed = MenuScreen(game_data=game_data).render(term)
            if keypressed == "n":
                # game_data.set_game_mode("new")
                GameScreen(game_data=game_data).render(term)
                pass
            elif keypressed == "t":
                # game_data.set_game_mode("tutorial")
                GameScreen(game_data=game_data).render(term)
                pass
            elif keypressed == "c":
                # game_data.set_game_mode("continue")
                # Load the saved game data
                pass
            elif keypressed == "a":
                AboutScreen(game_data=game_data).render(term)
            elif keypressed == "l":
                lang_selected = LanguageScreen(game_data=game_data).render(term)
                if lang_selected:
                    game_data.update_language(lang_selected)

    print(term.clear)
    sys.exit(0)


if __name__ == "__main__":
    main()
