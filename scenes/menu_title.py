import blessed

from assets import load_asset


def print_title(term: blessed.Terminal, rows: int, cols: int, color: str, term_color: str) -> set[tuple[int, int]]:
    """Draws the title in the terminal, returning the coordinates where it printed."""
    title_lines = load_asset("title.txt")
    title_width = max(term.length(title_line) for title_line in title_lines)
    title_height = len(title_lines)
    title_start_col = (cols - title_width) // 2
    title_start_row = (rows - title_height) // 4

    col, row = title_start_col, title_start_row
    for title_line in title_lines:
        print(f"{term.move_xy(col, row)}{getattr(term, color)}{title_line}{getattr(term, term_color)}", end="")
        row += 1

    return {(y + title_start_row, x + title_start_col) for x in range(title_width) for y in range(title_height)}
