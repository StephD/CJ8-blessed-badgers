from typing import Union

import blessed
import numpy as np
from blessed.keyboard import Keystroke

from modules.flying_square import Square
from modules.game_data import GameData
from scenes.menu_title import print_title


class MenuScreen:
    def __init__(self, game_data: GameData):
        num_squares = 4
        self.game_data = game_data
        self.squares = [Square() for _ in range(num_squares)]
        self.colors = self.game_data.data["game"]["colors"]["menu"].copy()
        self.term_color = f"{self.colors['text']}_on_{self.colors['bg']}"

    def render(self, term: blessed.Terminal) -> Union[Keystroke, str]:
        """Renders the start screen in the terminal."""
        cols, rows = term.width - 2, term.height - 2
        row, col = np.indices((rows, cols))
        row = row[::-1]
        row = (row - rows // 2) * 1 / 2
        col = (col - cols // 2) / 3 * 1 / 2

        with term.cbreak(), term.hidden_cursor():
            print(term.home + getattr(term, self.term_color) + term.clear)

            title_indices = print_title(term, rows, cols, self.colors["title"], self.term_color)
            menu_indices = self.print_text(term, rows, cols)

            old_indices = set()
            key_input = ""

            is_game_played = self.game_data.is_game_already_played()
            key_set = ["n", "c", "a", "q", "l"] if is_game_played else ["n", "a", "q", "l"]

            while key_input.lower() not in key_set:
                key_input = term.inkey(timeout=0.02)

                old_indices = self.render_flying_square(term, col, row, old_indices, title_indices, menu_indices)

            return key_input.lower()

    def get_language(self, *args):
        """Returns the language in the 'game_data' variable."""
        return self.game_data.get_str_in_language(*args)

    def print_text(self, term: blessed.Terminal, rows: int, cols: int) -> set[tuple[int, int]]:
        """Draws the menu in the terminal, returning the coordinates where it printed."""
        menu_items = [
            self.get_language("menu", "options", "new_game"),
            # self.get_language("menu", "options", "tutorial"),
            self.get_language("menu", "options", "continue"),
            self.get_language("menu", "options", "about"),
            self.get_language("menu", "options", "language"),
            self.get_language("menu", "options", "quit"),
        ]
        menu_width = len((" " * 5).join(menu_items))
        menu_start_col = (cols - menu_width) // 2
        menu_row = rows - 3

        print(term.move_xy(menu_start_col, menu_row), end="")

        for menu_item in menu_items:
            if (
                menu_item == self.get_language("menu", "options", "continue")
                and not self.game_data.data["game"]["is_game_already_played"]
            ):
                print(
                    f"{term.wheat4}{menu_item}" f"{getattr(term, self.term_color)}" f"{term.move_right(5)}",
                    end="",
                )
            else:
                print(
                    f"{menu_item[:-3]}{getattr(term,self.colors['choice'])}{menu_item[-3:]}"
                    f"{getattr(term,self.term_color)}"
                    f"{term.move_right(5)}",
                    end="",
                )

        return {(menu_row, x + menu_start_col) for x in range(menu_width)}

    def render_flying_square(self, term, col, row, old_indices, title_indices, menu_indices) -> set:
        """It will render the flying square around the screen"""
        print(getattr(term, self.colors["square"]))

        indices_to_be_painted = set()
        for square in self.squares:
            square.update(((col[0, 0], row[-1, 0]), (col[0, -1], row[0, 0])))
            indices_to_be_painted |= square.to_be_painted(row, col)

        for y_index, x_index in indices_to_be_painted - old_indices - title_indices - menu_indices:
            print(term.move_xy(x_index, y_index) + chr(9830), end="", flush=True)

        for y_index, x_index in old_indices - indices_to_be_painted - title_indices - menu_indices:
            print(term.move_xy(x_index, y_index) + " ", end="", flush=True)

        print(getattr(term, self.term_color))
        return indices_to_be_painted
