import blessed
import numpy as np

# from modules.language import Language
from scenes.menu_title import print_title

from .menu_screen import MenuScreen


class AboutScreen(MenuScreen):
    def render(self, term: blessed.Terminal) -> None:
        """Renders the start screen in the terminal."""
        cols, rows = term.width, term.height - 2
        row, col = np.indices((rows, cols))
        row = row[::-1]
        row = (row - rows // 2) * 1 / 2
        col = (col - cols // 2) / 3 * 1 / 2

        with term.cbreak(), term.hidden_cursor():
            print(term.home + term.clear)

            title_indices = print_title(term, rows, cols, self.menu_color_title, self.term_color)
            menu_indices = self.print_text(term, rows, cols)

            old_indices = set()
            key_input = ""
            while key_input.lower() not in ["r"]:
                key_input = term.inkey(timeout=0.02)

                old_indices = self.render_flying_square(term, col, row, old_indices, title_indices, menu_indices)
            return key_input

    def print_text(self, term: blessed.Terminal, rows: int, cols: int) -> set[tuple[int, int]]:
        """Draws the menu in the terminal, returning the coordinates where it printed."""
        sections = []
        sections.append(self.get_language("menu", "about", "about"))
        sections.append(self.get_language("menu", "about", "who"))
        sections.append("Version : 0.1")

        sections.append("")
        sections.append(self.get_language("menu", "actions", "return"))

        coordinates = set()
        for i, section in enumerate(sections):
            menu_width = len(section + " " * 2)
            menu_start_col = (cols - menu_width) // 2
            menu_row = rows - 5 + i

            print(term.move_xy(menu_start_col, menu_row), end="")
            print(
                f"{section[:-3]}"
                f"{getattr(term,self.menu_color_choice) if i==len(sections)-1 else getattr(term,self.term_color)}"
                f"{section[-3:]}{getattr(term,self.term_color)}"
            )

            coordinates = coordinates.union({(menu_row, x + menu_start_col) for x in range(menu_width)})

        return coordinates
