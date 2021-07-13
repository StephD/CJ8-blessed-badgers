import blessed

from modules.game import Game

# from modules.logger import log

# from scenes.scene import Scene


class GameScreen:
    def __init__(self, *args, **kwargs):
        self.game_mode = "normal"
        self.game = Game()

    def render(self, term: blessed.Terminal) -> None:
        """Renders the start screen in the terminal."""
        # cols, rows = term.width, term.height

        # self.game.render_layout()

        with term.cbreak(), term.hidden_cursor():
            val = ""
            while val.lower() != "q":
                val = term.inkey(timeout=3)
                if not val:
                    print("It sure is quiet in here ...")
                elif val.is_sequence:
                    print("got sequence: {0}.".format((str(val), val.name, val.code)))
                elif val:
                    print("got {0}.".format(val))

            print(f"bye!{term.normal}")

    def render_layout(self):
        pass
