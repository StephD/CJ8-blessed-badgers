import ast
from typing import Union

import blessed
import numpy as np
from blessed.keyboard import Keystroke

from modules.flying_square import Square
from modules.game_data import GameData
from modules.logger import log
from scenes.menu_title import print_title


class MenuScreen:
    def __init__(self, game_data: GameData):
        num_squares = 4
        self.game_data = game_data
        self.squares = [Square() for _ in range(num_squares)]
        gd = self.game_data.data
        self.menu_color_choice = f'{gd["game"]["colors"]["menu"]["choice"]}'
        self.menu_color_title = f'{gd["game"]["colors"]["menu"]["title"]}'
        self.menu_color_text = f'{gd["game"]["colors"]["menu"]["text"]}'
        self.menu_color_bg = f'{gd["game"]["colors"]["menu"]["bg"]}'
        self.menu_color_square = f'{gd["game"]["colors"]["menu"]["square"]}'
        self.term_color = f"{self.menu_color_text}_on_{self.menu_color_bg}"

    def render(self, term: blessed.Terminal) -> Union[Keystroke, str]:
        """Renders the start screen in the terminal."""
        cols, rows = term.width, term.height
        row, col = np.indices((rows, cols))
        row = row[::-1]
        row = (row - rows // 2) * 1 / 2
        col = (col - cols // 2) / 3 * 1 / 2
        cols, rows = term.width - 2, term.height - 2

        with term.cbreak(), term.hidden_cursor():
            print(term.home + getattr(term, self.term_color) + term.clear)

            title_indices = print_title(term, rows, cols, self.menu_color_title, self.term_color)
            menu_indices = self.print_text(term, rows, cols)

            old_indices = set()
            key_input = ""
            while key_input.lower() not in ["n", "c", "t", "a", "q", "l"]:
                key_input = term.inkey(timeout=0.02)

                old_indices = self.render_flying_square(term, col, row, old_indices, title_indices, menu_indices)

            return key_input.lower()

    def get_language(self, *args):
        return self.game_data.get_str_in_language(*args)

    def print_text(self, term: blessed.Terminal, rows: int, cols: int) -> set[tuple[int, int]]:
        """Draws the menu in the terminal, returning the coordinates where it printed."""
        menu_items = [
            self.get_language("menu", "options", "new_game"),
            self.get_language("menu", "options", "tutorial"),
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
            print(
                f"{menu_item[:-3]}{getattr(term,self.menu_color_choice)}{menu_item[-3:]}"
                f"{getattr(term,self.term_color)}"
                f"{term.move_right(5)}",
                end="",
            )

        return {(menu_row, x + menu_start_col) for x in range(menu_width)}

    def render_flying_square(self, term, col, row, old_indices, title_indices, menu_indices) -> set:
        """It will render the flying square around the screen"""
        print(getattr(term, self.menu_color_square))

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
