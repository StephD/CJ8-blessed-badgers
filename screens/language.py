import blessed


def make_menu(term: blessed.Terminal, rows: int, cols: int) -> set[tuple[int, int]]:
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
