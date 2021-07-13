# TODO


def draw_map(self) -> str:
    """Draw a map and the player."""
    width = self.term.width // 2
    height = self.term.height // 2

    box = "┌" + "─" * width + "┐\n"
    for i in range(height):
        box += "│" + " " * width + "│\n"

    box += "└" + "─" * width + "┘"

    # Add Walls to obstacles
    obstacles = []
    # For left & right side walls.
    for i in range(width):
        obstacles.append((i, 0))
        obstacles.append((i, height + 1))

    # For top & bottom walls.
    for i in range(height + 1):
        obstacles.append((0, i))
        obstacles.append((width, i))

    self.obstacles = set(obstacles)

    self.pos_x = width // 2
    self.pos_y = height // 2
    box += self.term.move_xy(self.pos_x, self.pos_y) + self.player

    return box
