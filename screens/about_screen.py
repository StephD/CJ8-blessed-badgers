import blessed
import numpy as np

# from modules.language import Language
from scenes import make_title

from .menu_screen import MenuScreen


class AboutScreen(MenuScreen):
    def render(self, term: blessed.Terminal) -> None:
        """Renders the start screen in the terminal."""
        cols, rows = term.width, term.height
        rows -= 2
        cols -= 2
        row, col = np.indices((rows, cols))
        row = row[::-1]
        row = (row - rows // 2) * 1 / 2
        col = (col - cols // 2) / 3 * 1 / 2

        with term.cbreak(), term.hidden_cursor():
            print(term.home + term.clear)

            title_indices = make_title(term, rows, cols)
            menu_indices = self.make_menu(term, rows, cols)

            old_indices = set()
            key_input = ""
            while key_input.lower() not in ["b"]:
                key_input = term.inkey(timeout=0.02)

                old_indices = self.render_flying_square(term, col, row, old_indices, title_indices, menu_indices)
            return key_input

    def make_menu(self, term: blessed.Terminal, rows: int, cols: int) -> set[tuple[int, int]]:
        """Draws the menu in the terminal, returning the coordinates where it printed."""
        # divide menu to sections: What, Who, Why
        what = "This is a gamefied learning experience for young developers"
        who = "Made by young developers: Blessed badgers"
        why = "For fun and codejam :)"
        exit_text = "press [b] to return to Main menu"
        sections = [what, who, why, exit_text]
        coordinates = set()
        for i, section in enumerate(sections):
            menu_width = len(section + " " * 2)
            menu_start_col = (cols - menu_width) // 2
            menu_row = rows - 5 + i
            print(term.move_xy(menu_start_col, menu_row), end="")
            print(section)
            coordinates = coordinates.union({(menu_row, x + menu_start_col) for x in range(menu_width)})
        return coordinates
