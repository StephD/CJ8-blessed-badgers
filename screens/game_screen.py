import sys
from typing import Union

import blessed

from modules.game import Game
from modules.game_data import GameData
from modules.logger import log
from scenes.entity import SubtractableDict

Bounds = tuple[int, int, int, int]


def _lies_within_bounds(bounds: Bounds, point: tuple[int, int]) -> bool:
    """Check whether the given point lies within the given bounds."""
    start_i, end_i, start_j, end_j = bounds
    i, j = point
    return start_i < i < end_i and start_j < j < end_j


def chunk(string: str, width: int) -> list[str]:
    """Split the given string into a list of lines, where the length of each line is less than the given width."""
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
        # self.scene_bounds: Bounds = ...
        # self.sidebar_bounds: Bounds = ...
        # self.message_bar_bounds: Bounds = ...

    def init_bound(self, term: blessed.Terminal):
        width, height = term.width, term.height

        # The layout have to be fixed and the size of the scene
        # Top - Bottom - Left - Right
        self.sidebar_bounds = (1, height - 2, int(3 / 4 * width) + 1, width - 3)
        self.scene_bounds = (1, int(3 / 4 * height), 2, int(3 / 4 * width) - 1)
        self.message_bar_bounds = (int(3 / 4 * height) + 1, height - 2, 2, int(3 / 4 * width) - 1)

        self._render_dict(term, self._make_border((0, height - 1, 0, width - 1), tuple("╔╗╚╝║═")))

    def render(self, term: blessed.Terminal) -> None:
        """Renders the start screen in the terminal."""
        self.init_bound(term)

        key_input = ""
        with term.cbreak(), term.hidden_cursor():
            # Render layout
            self.render_layout(term)
            # Render scene
            self.render_scene(term)
            # Render scene entities
            # Render sidebar content
            self.render_sidebar_content(term)
            # Render message in the bottom bar
            # while not in esc menu and key different then 'q'
            while key_input.lower() != "q":
                key_input = term.inkey(timeout=3)
                if not key_input:
                    continue
                elif key_input.is_sequence:
                    self.game.move_player(key_input.name)
                    self.render_scene(term)
                elif key_input:
                    self.game.move_player(key_input)
                    self.render_scene(term)
        # Remove all
        """
        self.currently_rendered = self.currently_rendered
                                    - self.currently_rendered
        """
        # self.currently_rendered = SubtractableDict()

    def render_layout(self, term: blessed.Terminal) -> None:
        self._render_dict(term, self._make_border(self.sidebar_bounds, tuple("┌┐└┘│─")))
        self._render_dict(term, self._make_border(self.scene_bounds, tuple("┌┐└┘│─")))
        self._render_dict(term, self._make_border(self.message_bar_bounds, tuple("┌┐└┘│─")))

    # Render scene need to be pickup from a file
    def render_scene(self, term: blessed.Terminal):
        to_be_rendered = self._make_scene(self.scene_bounds, self.game.get_to_be_rendered())

        self._render_dict(term, to_be_rendered - self.currently_rendered)
        # What is this?
        self._render_dict(term, {(i, j): " " for i, j in self.currently_rendered - to_be_rendered})

        self.currently_rendered = to_be_rendered

    def render_sidebar_content(self, term: blessed.Terminal):
        start_y, end_y, start_x, end_x = self.sidebar_bounds

        # Look like it avoid the cursor to be in a random pos
        self._render_dict(
            term, {(i, j): " " for i in range(*self.sidebar_bounds[:2]) for j in range(*self.sidebar_bounds[2:])}
        )

        log(str(start_x), "x")
        log(str(start_y), "y")
        term.move_yx(start_y, start_x)

        sidebar_content = self.game.get_sidebar_content()
        panel_width = end_x - start_x
        log(str(panel_width), "panel_width")
        for line in chunk(sidebar_content, panel_width):
            print(line, end="", flush=True)
            print(term.move_left(len(line)) + term.move_down, end="", flush=True)

    def render_messagebar_content(self, term: blessed.Terminal):
        start_y, end_y, start_x, end_x = self.message_bar_bounds
        pass

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
    def _render_dict(term: blessed.Terminal, data: Union[dict, SubtractableDict]) -> None:
        for (i, j), char in data.items():
            print(term.move_yx(i, j) + char, end="", flush=True)
