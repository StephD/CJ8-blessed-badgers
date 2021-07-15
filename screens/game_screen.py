import sys
from time import sleep
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
        self.stories_id = 1
        # self.scene_bounds: Bounds = ...
        # self.sidebar_bounds: Bounds = ...
        # self.message_bar_bounds: Bounds = ...

    def init_bound(self, term: blessed.Terminal):
        """Initialize the layout side and frame size+position"""
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

            # Render message in the bottom bar
            while self.game.story[str(self.stories_id)] != "":
                self.render_messagebar_content(term, self.game.story[str(self.stories_id)])
                term.inkey(timeout=5)
                if self.stories_id == 1:
                    break
                self.stories_id += 1

            # Clean the message bar
            self.render_sidebar_content(term)

            # while not in esc menu and key different then 'q'
            while key_input.lower() != "q":
                key_input = term.inkey(timeout=3)
                if not key_input:
                    continue
                elif key_input.is_sequence:
                    self.game.move_player(key_input.name)
                    self.render_scene(term)
                    self.render_messagebar_content(term)
                elif key_input:
                    self.game.move_player(key_input)
                    self.render_scene(term)
                    self.render_messagebar_content(term)

        # """
        # self.currently_rendered = self.currently_rendered
        #                             - self.currently_rendered
        # """
        # Remove all
        # self.currently_rendered = SubtractableDict()

    def render_layout(self, term: blessed.Terminal) -> None:
        """Render the 3 frames"""
        self._render_dict(term, self._make_border(self.scene_bounds, tuple("┌┐└┘│─")))
        self._render_dict(term, self._make_border(self.sidebar_bounds, tuple("┌┐└┘│─")))
        self._render_dict(term, self._make_border(self.message_bar_bounds, tuple("┌┐└┘│─")))

    # Render scene need to be pickup from a file
    def render_scene(self, term: blessed.Terminal):
        """Render the scene area. Design the level"""
        to_be_rendered = self._make_scene(self.scene_bounds, self.game.get_to_be_rendered())

        self._render_dict(term, to_be_rendered - self.currently_rendered)

        # Clean the content around what need to be rendered
        self._render_dict(term, {(i, j): " " for i, j in self.currently_rendered - to_be_rendered})

        self.currently_rendered = to_be_rendered

    def render_sidebar_content(self, term: blessed.Terminal):
        """Render the content of the sidebar. Will display all the game data"""
        start_y, end_y, start_x, end_x = self.sidebar_bounds
        panel_width = end_x - start_x
        sidebar_content = self.game.get_sidebar_content()

        # Clean the content of the sidebar
        self._render_dict(term, {(y, x): " " for y in range(start_y + 1, end_y) for x in range(start_x + 1, end_x)})

        print(term.move_yx(start_y + 2, start_x + 2), end="")

        for data_key, data_obj in sidebar_content.items():
            if data_key == "game_data":
                print(
                    term.orangered
                    + "Game data"
                    + " " * (panel_width - len("Game data : "))
                    + term.move_left(panel_width - 3)
                    + term.move_down
                    + term.normal,
                    end="",
                )
            elif data_key == "player_data":
                print("Game data : ", end="")
            for key, value in data_obj.items():
                for line in chunk(f"{key} : {value}", panel_width):
                    print(line, end="", flush=True)
                    print(term.move_left(len(line)) + term.move_down, end="", flush=True)
                print(term.move_down, end="", flush=True)

    def render_messagebar_content(self, term: blessed.Terminal, message: str = ""):
        start_y, end_y, start_x, end_x = self.message_bar_bounds
        panel_height = end_y - start_y
        panel_width = end_x - start_x

        # Clean the content
        print(term.move_xy(start_x + 4, start_y + round(panel_height / 2)), end="")
        print(" " * (panel_width - 6), end="", flush=True)

        print(term.move_left(panel_width - 7), end="")
        for letter in message:
            print(letter, end="", flush=True)
            sleep(0.05)

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
