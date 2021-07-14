from typing import Union
import sys

import blessed

from modules.game import Game
from modules.game_data import GameData
from modules.logger import log
from scenes.entity import SubtractableDict


Bounds = tuple[int, int, int, int]


def _lies_within_bounds(bounds: Bounds, point: tuple[int, int]):
    start_i, end_i, start_j, end_j = bounds
    i, j = point
    return start_i < i < end_i and start_j < j < end_j


def chunk(string: str, width: int) -> list[str]:
    lines = string.splitlines()
    chunked = []
    for line in lines:
        chunked.append("")
        words = line.split()
        if any(len(word) >= width for word in words):
            raise ValueError("Insufficient width")
        for word in words:
            if len(f"{chunked[-1]} {word}") >= width:
                chunked.append("")
            chunked[-1] += word + " "
    return [line.strip() for line in chunked]


class GameScreen:
    def __init__(self, game_data: GameData, *args, **kwargs):
        self.game_data = game_data
        self.game = Game(game_data)
        self.currently_rendered = SubtractableDict()
        self.scene_bounds: Bounds = ...
        self.sidebar_bounds: Bounds = ...
        self.action_bar_bounds: Bounds = ...

    def render(self, term: blessed.Terminal) -> None:
        """Renders the start screen in the terminal."""
        with term.cbreak(), term.hidden_cursor():
            # Render layout
            # Render scene
            # Render entities
            # Render message
            # Render gamedata
            self.render_layout(term)
            val = ""
            while val.lower() != "q":
                self.render_layout(term)
                self.render_scene(term)
                self.render_sidebar(term)
                val = term.inkey(timeout=3)
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
        width, height = term.width, term.height

        self.sidebar_bounds = (1, height - 2, int(3 / 4 * width), width - 2)
        self.scene_bounds = (1, int(3 / 4 * height), 1, int(3 / 4 * width) - 1)
        self.action_bar_bounds = (int(3 / 4 * height) + 1, height - 2, 1, int(3 / 4 * width) - 1)

        self._render_dict(term, self._make_border((0, height - 1, 0, width - 1), tuple("╔╗╚╝║═")))
        self._render_dict(term, self._make_border(self.sidebar_bounds, tuple("┌┐└┘│─")))
        self._render_dict(term, self._make_border(self.scene_bounds, tuple("┌┐└┘│─")))
        self._render_dict(term, self._make_border(self.action_bar_bounds, tuple("┌┐└┘│─")))

    def render_scene(self, term: blessed.Terminal):
        to_be_rendered = self._make_scene(self.scene_bounds, self.game.get_to_be_rendered())
        self._render_dict(term, to_be_rendered - self.currently_rendered)
        self._render_dict(term, {(i, j): " " for i, j in self.currently_rendered - to_be_rendered})
        self.currently_rendered = to_be_rendered

    def render_sidebar(self, term: blessed.Terminal):
        start_i, end_i, start_j, end_j = self.sidebar_bounds
        self._render_dict(
            term, {(i, j): " " for i in range(*self.sidebar_bounds[:2]) for j in range(*self.sidebar_bounds[2:])}
        )
        sidebar_content = self.game.get_sidebar_content()
        panel_width = end_j - start_j
        print(term.move_yx(start_i, start_j))
        for line in chunk(sidebar_content, panel_width):
            print(line, end="", flush=True)
            print(term.move_left(len(line)) + term.move_down, end="", flush=True)

    @staticmethod
    def _make_border(bounds: Bounds, charset: tuple[str, str, str, str, str, str]) -> SubtractableDict:
        start_i, end_i, start_j, end_j = bounds
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
    def _make_scene(bounds: Bounds, game_map: SubtractableDict) -> SubtractableDict:

        start_i, end_i, start_j, end_j = bounds
        scene_panel_width = end_j - start_j
        scene_panel_height = end_i - start_i
        clipped_map = SubtractableDict()

        scene_start_i = min(coordinate[0] for coordinate in game_map)
        scene_end_i = max(coordinate[0] for coordinate in game_map)
        scene_start_j = min(coordinate[1] for coordinate in game_map)
        scene_end_j = max(coordinate[1] for coordinate in game_map)

        scene_height = scene_end_i - scene_start_i
        scene_width = scene_end_j - scene_start_j

        central_i, central_j = (scene_height // 2, scene_width // 2)

        for (i, j), char in game_map.items():
            new_i = i - central_i + scene_panel_height // 2
            new_j = j - central_j + scene_panel_width // 2
            if _lies_within_bounds(bounds, (new_i, new_j)):
                clipped_map[new_i, new_j] = char

        return clipped_map

    @staticmethod
    def _render_dict(term: blessed.Terminal, data: Union[dict, SubtractableDict]):
        for (i, j), char in data.items():
            print(term.move_yx(i, j) + char, end="", flush=True)
