import blessed


def make_menu(term: blessed.Terminal, rows: int, cols: int) -> set[tuple[int, int]]:
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
