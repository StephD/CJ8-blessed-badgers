from typing import Union

import blessed
import numpy as np
from blessed.keyboard import Keystroke

from modules.flying_square import Square
from modules.game_data import GameData
from modules.language import Language
from scenes.menu_title import print_title


class MenuScreen:
    def __init__(self):
        num_squares = 4
        self.squares = [Square() for _ in range(num_squares)]
        self.game_data = GameData()
        self.language = Language()

    def render(self, term: blessed.Terminal) -> Union[Keystroke, str]:
        """Renders the start screen in the terminal."""
        cols, rows = term.width, term.height
        row, col = np.indices((rows, cols))
        row = row[::-1]
        row = (row - rows // 2) * 1 / 2
        col = (col - cols // 2) / 3 * 1 / 2
        cols, rows = term.width - 2, term.height - 2

        with term.cbreak(), term.hidden_cursor():
            print(term.home + term.lightskyblue_on_gray20 + term.clear)

            title_indices = print_title(term, rows, cols)
            menu_indices = self.print_text(term, rows, cols)

            old_indices = set()
            key_input = ""
            while key_input.lower() not in ["n", "c", "t", "a", "q", "l"]:
                key_input = term.inkey(timeout=0.02)

                old_indices = self.render_flying_square(term, col, row, old_indices, title_indices, menu_indices)

            return key_input.lower()

    def print_text(self, term: blessed.Terminal, rows: int, cols: int) -> set[tuple[int, int]]:
        """Draws the menu in the terminal, returning the coordinates where it printed."""
        menu_items = [
            self.language.get("menu", "options", "new_game"),
            self.language.get("menu", "options", "tutorial"),
            self.language.get("menu", "options", "continue"),
            self.language.get("menu", "options", "about"),
            self.language.get("menu", "options", "language"),
            self.language.get("menu", "options", "quit"),
        ]
        menu_width = len((" " * 5).join(menu_items))
        menu_start_col = (cols - menu_width) // 2
        menu_row = rows - 3

        print(term.move_xy(menu_start_col, menu_row), end="")

        for menu_item in menu_items:
            print(menu_item + term.move_right(5), end="")

        return {(menu_row, x + menu_start_col) for x in range(menu_width)}

    def render_flying_square(self, term, col, row, old_indices, title_indices, menu_indices) -> set:
        """It will render the flying square around the screen"""
        indices_to_be_painted = set()
        for square in self.squares:
            square.update(((col[0, 0], row[-1, 0]), (col[0, -1], row[0, 0])))
            indices_to_be_painted |= square.to_be_painted(row, col)

        for y_index, x_index in indices_to_be_painted - old_indices - title_indices - menu_indices:
            print(term.move_xy(x_index, y_index) + chr(8226), end="", flush=True)

        for y_index, x_index in old_indices - indices_to_be_painted - title_indices - menu_indices:
            print(term.move_xy(x_index, y_index) + " ", end="", flush=True)

        return indices_to_be_painted
