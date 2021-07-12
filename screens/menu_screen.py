from typing import Union

import blessed
import numpy as np
from blessed.keyboard import Keystroke

from modules.flying_square import Square
from scenes.menu_title import make_title


class MenuScreen:
    def __init__(self):
        num_squares = 6
        self.squares = [Square() for _ in range(num_squares)]

    def render(self, term: blessed.Terminal) -> Union[Keystroke, str]:
        """Renders the start screen in the terminal."""
        cols, rows = term.width, term.height
        rows -= 2
        cols -= 2

        with term.cbreak(), term.hidden_cursor():
            print(term.home + term.on_blue + term.clear)

            row, col = np.indices((rows, cols))
            row = row[::-1]
            row = (row - rows // 2) * 1 / 2
            col = (col - cols // 2) / 3 * 1 / 2

            old_indices = set()

            title_indices = make_title(term, rows, cols)
            menu_indices = self.make_menu(term, rows, cols)

            key_input = ""
            while key_input.lower() not in ["n", "c", "t", "a", "q", "l"]:
                key_input = term.inkey(timeout=0.02)

                # Print the flying square
                indices_to_be_painted = set()
                for square in self.squares:
                    square.update(((col[0, 0], row[-1, 0]), (col[0, -1], row[0, 0])))
                    indices_to_be_painted |= square.to_be_painted(row, col)

                for y_index, x_index in indices_to_be_painted - old_indices - title_indices - menu_indices:
                    print(term.move_xy(x_index, y_index) + chr(8226), end="", flush=True)

                for y_index, x_index in old_indices - indices_to_be_painted - title_indices - menu_indices:
                    print(term.move_xy(x_index, y_index) + " ", end="", flush=True)

                old_indices = indices_to_be_painted

            return key_input

    def make_menu(self, term: blessed.Terminal, rows: int, cols: int) -> set[tuple[int, int]]:
        """Draws the menu in the terminal, returning the coordinates where it printed."""
        menu_items = [
            "New Game [n]",
            "Tutorial [t]",
            "Continue [c]",
            "About [a]",
            "Language [l]",
            "Quit [q]",
        ]
        menu_width = len((" " * 5).join(menu_items))
        menu_start_col = (cols - menu_width) // 2
        menu_row = rows - 3

        print(term.move_xy(menu_start_col, menu_row), end="")

        for menu_item in menu_items:
            print(menu_item + term.move_right(5), end="")

        return {(menu_row, x + menu_start_col) for x in range(menu_width)}