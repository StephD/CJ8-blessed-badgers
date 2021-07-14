import sys

import blessed

from modules.game import Game
from modules.game_data import GameData
from modules.logger import log
from scenes.entity import SubtractableDict


class GameScreen:
    def __init__(self, game_data: GameData, *args, **kwargs):
        self.game_data = game_data
        self.game = Game(game_data)
        self.currently_rendered = SubtractableDict()

    def render(self, term: blessed.Terminal) -> None:
        """Renders the start screen in the terminal."""
        with term.cbreak(), term.hidden_cursor():
            # Render layout
            self.render_layout(term)
            # Render scene
            # Render entities
            # Render message
            # Render gamedata
            val = ""
            while val.lower() != "q":
                val = term.inkey()
                if not val:
                    continue
                elif val.is_sequence:
                    self.game.move_player(val.name)
                elif val:
                    self.game.move_player(val)
        # Remove all
        """
        self.currently_rendered = self.currently_rendered
                                    - self.currently_rendered
        """
        self.currently_rendered = SubtractableDict()

    def render_layout(self, term: blessed.Terminal) -> None:
        to_be_rendered = self.game.get_to_be_rendered()
        for (i, j), char in (to_be_rendered - self.currently_rendered).items():
            print(term.move_yx(i, j) + char)
        for (i, j) in self.currently_rendered - to_be_rendered:
            print(term.move_yx(i, j) + " ")
        self.currently_rendered = to_be_rendered
