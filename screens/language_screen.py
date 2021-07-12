import blessed
import numpy as np

from scenes import make_title

from .menu_screen import MenuScreen


class LanguageScreen(MenuScreen):
    def render(self, term: blessed.Terminal) -> None:
        """Renders the start screen in the terminal."""
        cols, rows = term.width, term.height
        row, col = np.indices((rows, cols))
        row = row[::-1]
        row = (row - rows // 2) * 1 / 2
        col = (col - cols // 2) / 3 * 1 / 2
        cols, rows = term.width - 2, term.height - 2

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
        en = "Select English" + " " * 5 + "[1]"
        ru = "выбрать русский" + " " * 4 + "[2]"
        es = "Elegir español" + " " * 5 + "[3]"
        fr = "Elija francés" + " " * 6 + "[4]"
        de = "Wählen Sie Deutsch" + " " + "[5]"
        exit_text = "Exit" + " " * 15 + "[b]"
        sections = [en, ru, es, fr, de, exit_text]
        coordinates = set()
        for i, section in enumerate(sections):
            menu_width = len(section + " " * 0)
            menu_start_col = (cols - menu_width) // 2
            menu_row = rows - 10 + i
            print(term.move_xy(menu_start_col, menu_row), end="")
            print(section)
            coordinates = coordinates.union({(menu_row, x + menu_start_col) for x in range(menu_width)})
        return coordinates
