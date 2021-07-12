import blessed

from assets import load_asset


def make_title(term: blessed.Terminal, rows: int, cols: int) -> set[tuple[int, int]]:
    """Draws the title in the terminal, returning the coordinates where it printed."""
    title_lines = load_asset("title.txt")
    title_width = max(term.length(title_line) for title_line in title_lines)
    title_height = len(title_lines)
    title_start_col = (cols - title_width) // 2
    title_start_row = (rows - title_height) // 4
    print(term.move_xy(title_start_col, title_start_row), end="")
    for title_line in title_lines:
        print(title_line + term.move_down + term.move_left(len(title_line)), end="")

    return {(y + title_start_row, x + title_start_col) for x in range(title_width) for y in range(title_height)}
