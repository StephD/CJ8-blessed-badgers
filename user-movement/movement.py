from blessed import Terminal


class Game:
    """Basic Game."""

    player = "@"

    def __init__(self, term, obstacles=set()) -> None:
        self.term = term
        self.pos_x = 2
        self.pos_y = 2
        self.obstacles = obstacles

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

    def move_player(self, mov) -> None:
        """Move player with"""
        # Make a copy of the position of the player.
        pos_x, pos_y = self.pos_x, self.pos_y

        # Erase the current position.
        term_erase = self.term.move_xy(pos_x, pos_y) + " "

        # Update the position.
        if mov == "\x1b[A":
            pos_y -= 1
        if mov == "\x1b[B":
            pos_y += 1
        if mov == "\x1b[D":
            pos_x -= 1
        if mov == "\x1b[C":
            pos_x += 1

        if (pos_x, pos_y) not in self.obstacles:
            term_player = self.term.move_xy(pos_x, pos_y) + "@"
            print(term_erase + term_player, end="", flush=True)
            # Update the position of the player.
            self.pos_x, self.pos_y = pos_x, pos_y


def main() -> None:
    """Main"""
    term = Terminal()
    inp = ""
    game = Game(term)

    print(term.home + term.clear + game.draw_map())
    with term.cbreak(), term.hidden_cursor():
        while inp != "q":
            inp = term.inkey()
            print(str(inp))
            game.move_player(inp)
        print(term.clear, "BYE!")


if __name__ == "__main__":
    main()
