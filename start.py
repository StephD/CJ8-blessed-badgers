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
    menu_screen = MenuScreen(game_data=game_data)
    about_screen = AboutScreen(game_data=game_data)
    language_screen = LanguageScreen(game_data=game_data)
    # game_screen = GameScreen(game_data=game_data)

    keypressed = None
    with term.fullscreen(), term.cbreak():
        while keypressed != "q":
            keypressed = menu_screen.render(term)
            print(term.clear)
            if keypressed == "n":  # New game
                game_data.load_game("new")
                # game_data.set_game_level(1)
                # game_data.set_game_already_played(False)
                game_screen = GameScreen(game_data=game_data)
                game_screen.render(term)
            elif keypressed == "c":
                game_data.load_game("saved")
                game_screen = GameScreen(game_data=game_data)
                game_screen.render(term)
            elif keypressed == "a":
                about_screen.render(term)
            elif keypressed == "l":
                lang_selected = language_screen.render(term)
                if lang_selected:
                    game_data.set_language(lang_selected)

    print(term.normal)
    sys.exit(0)


if __name__ == "__main__":
    main()
