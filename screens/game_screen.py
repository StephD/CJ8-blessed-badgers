from typing import Union

import blessed

from modules.game import Game
from scenes.entity import SubtractableDict


class GameScreen:
    def __init__(self, *args, **kwargs):
        self.game_mode = "normal"
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

        width, height = term.width, term.height

        sidebar_bounds: tuple[int, int, int, int] = (1, height - 2, int(3 / 4 * width), width - 2)
        scene_bounds = (1, int(3 / 4 * height), 1, int(3 / 4 * width) - 1)
        action_bar_bounds = (int(3 / 4 * height) + 1, height - 2, 1, int(3 / 4 * width) - 1)

        self._render_dict(term, self._make_border(0, height - 1, 0, width - 1, tuple("╔╗╚╝║═")))
        self._render_dict(term, self._make_border(*sidebar_bounds, tuple("┌┐└┘│─")))
        self._render_dict(term, self._make_border(*scene_bounds, tuple("┌┐└┘│─")))
        self._render_dict(term, self._make_border(*action_bar_bounds, tuple("┌┐└┘│─")))

        to_be_rendered = self.game.get_to_be_rendered()
        # self._render_dict(term, to_be_rendered - self.currently_rendered)
        # self._render_dict(term, {(i, j): " " for i, j in self.currently_rendered - to_be_rendered})
        self.currently_rendered = to_be_rendered

    @staticmethod
    def _make_border(
        start_i: int, end_i: int, start_j: int, end_j: int, charset: tuple[str, str, str, str, str, str]
    ) -> SubtractableDict:
        top_left, top_right, bottom_left, bottom_right, vertical, horizontal = charset
        return SubtractableDict(
            {
                (start_i, start_j): top_left,
                (start_i, end_j): top_right,
                (end_i, start_j): bottom_left,
                (end_i, end_j): bottom_right,
            }
            | {(i, j): vertical for i in range(start_i + 1, end_i) for j in (start_j, end_j)}
            | {(i, j): horizontal for i in (start_i, end_i) for j in range(start_j + 1, end_j)}
        )

    @staticmethod
    def _render_dict(term: blessed.Terminal, data: Union[dict, SubtractableDict]):
        for (i, j), char in data.items():
            print(term.move_yx(i, j) + char, end="")
