import blessed

from modules.game import Game
from scenes.entity import SubtractableDict


class GameScreen:
    def __init__(self, *args, **kwargs):
        self.game_data = args["game_data"]
        self.game = Game()
        self.currently_rendered = SubtractableDict()

    def render(self, term: blessed.Terminal) -> None:
        """Renders the start screen in the terminal."""
        with term.cbreak(), term.hidden_cursor():
            val = ""
            while val.lower() != "q":
                self.render_layout(term)
                val = term.inkey(timeout=3)
                if not val:
                    continue
                elif val.is_sequence:
                    self.game.move_player(val.name)
                    continue
                elif val:
                    self.game.move_player(val)
                    continue

            print(f"bye!{term.normal}")

    def render_layout(self, term: blessed.Terminal) -> None:
        to_be_rendered = self.game.get_to_be_rendered()
        for (i, j), char in (to_be_rendered - self.currently_rendered).items():
            print(term.move_yx(i, j) + char)
        for (i, j) in self.currently_rendered - to_be_rendered:
            print(term.move_yx(i, j) + " ")
        self.currently_rendered = to_be_rendered
