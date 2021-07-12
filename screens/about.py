import blessed


def make_menu(term: blessed.Terminal, rows: int, cols: int) -> set[tuple[int, int]]:
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
