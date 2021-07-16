from time import sleep

import blessed

from modules.game import Game
from modules.game_data import GameData
from modules.logger import log

Bounds = tuple[int, int, int, int]
RenderableCoordinate = tuple[int, int, str]


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
            # If adding the current word to the current line would cause overflow, add a fresh string to the list.
            if len(f"{chunked[-1]} {word}") >= width:
                chunked.append("")
            # Add the current word to the current line, with a space.
            chunked[-1] += word + " "
    return [line.strip() for line in chunked]


class GameScreen:
    def __init__(self, game_data: GameData):
        self.game_data = game_data
        self.game = Game(game_data)
        self.currently_rendered: set[RenderableCoordinate] = set()
        self.stories_id = 1
        self.colors = self.game_data.data["game"]["colors"]["game"].copy()
        self.term_color = f"{self.colors['text']}_on_{self.colors['bg']}"
        self.sidebar_bounds: Bounds = ...
        self.scene_bounds: Bounds = ...
        self.message_bar_bounds: Bounds = ...

    def init_bound(self, term: blessed.Terminal):
        """Initialize the layout side and frame size+position"""
        width, height = term.width, term.height

        # The layout have to be fixed and the size of the scene
        # Top - Bottom - Left - Right
        self.sidebar_bounds = (1, height - 2, int(3 / 4 * width) + 1, width - 3)
        self.scene_bounds = (1, int(3 / 4 * height), 2, int(3 / 4 * width) - 1)
        self.message_bar_bounds = (int(3 / 4 * height) + 1, height - 2, 2, int(3 / 4 * width) - 1)

        # Render the screen border
        self._render_dict(term, self._make_border((0, height - 1, 0, width - 1), tuple("╔╗╚╝║═")))

    def render(self, term: blessed.Terminal) -> None:
        """Renders the start screen in the terminal."""
        self.init_bound(term)

        key_input = ""
        with term.cbreak(), term.hidden_cursor():
            self.render_layout(term)

            # Render story messages in the bottom bar
            if not self.game_data.is_game_already_played():
                while self.game.story[str(self.stories_id)] != "":
                    self.render_messagebar_content(term, self.game.story[str(self.stories_id)] + "  [ENTER]", 0.03)

                    key_input = ""
                    while key_input != "enter":
                        key_input = term.inkey()
                        if key_input.is_sequence and key_input.name == "KEY_ENTER":
                            key_input = "enter"

                    # Still have to adjust the story display
                    if self.stories_id == 1:
                        # render the player
                        pass
                    elif self.stories_id == 2:
                        # don't know yet
                        self.render_scene(term)
                    elif self.stories_id == 3:
                        self.render_scene(term)
                    elif self.stories_id == 4:
                        self.render_scene(term)
                    elif self.stories_id == 5:
                        break

                    self.stories_id += 1
                    self.game_data.set_game_already_played(True)
            else:
                # Make all the render
                self.stories_id = 5
                self.render_scene(term)

            self.render_sidebar_content(term)
            # Clean message bar
            self.render_messagebar_content(term)

            # player movement and exit or confirm exit.
            while 1:
                player_will_move = False
                key_input = term.inkey()
                if key_input.is_sequence:
                    # Esc menu
                    if key_input.name in ["KEY_ESCAPE"]:
                        self.render_messagebar_content(
                            term, self.game_data.get_str_in_language("messages", "game", "actions", "esc"), 0
                        )
                        while key_input.lower() not in ["q", "s", "c", "esc"]:
                            key_input = term.inkey()
                            if key_input == "s":
                                self.game_data.save_game()
                                self.render_messagebar_content(term, "Saving in progress")
                                sleep(0.8)
                                self.render_messagebar_content(term, "Saving is done")
                                sleep(0.8)
                            elif key_input.lower() == "q":
                                # self.game_data.save_game()
                                self.render_messagebar_content(term, "bye ..")
                                sleep(0.8)
                                # It's not strong to return like this?
                                return
                        self.render_messagebar_content(term, "")
                    elif key_input.name in ["KEY_DOWN", "KEY_UP", "KEY_LEFT", "KEY_RIGHT"]:
                        key_input = key_input.name
                        player_will_move = True
                elif key_input in ["j", "k", "h", "l"]:
                    player_will_move = True

                if player_will_move:
                    # msg from game.
                    entity_meeted = self.game.move_player(key_input)
                    self.render_scene(term)
                    self.render_messagebar_content(term)
                    if entity_meeted:
                        log(entity_meeted, "entity_meeted")
                    if entity_meeted == "D":
                        # Why this is rendering two times ?
                        if self.game_data.get_inventory_item_by_key("keys") > 0:
                            # get room id
                            self.game_data.unlock_door(self.game_data.data["player"]["current_room"])
                            self.game_data.dec_inventory_item_by_key("keys")
                            self.render_sidebar_content(term)
                            # self.render_messagebar_content(term, self.game.story["11"])
                            if self.game_data.data["room"]["1"]["is_door_unlocked"]:
                                self.render_messagebar_content(term, "Congrats you have solved the first level.")
                                sleep(1)
                                return
                        else:
                            self.render_messagebar_content(
                                term, self.game_data.get_str_in_language("entities", "key", "close")
                            )
                            # self.render_messagebar_content(term, self.game.story["9"])

                        # self.render_messagebar_content(term, self.game.story[str(self.stories_id)])
                    elif entity_meeted == "X":
                        # self.render_messagebar_content(term, self.game.story["10"])
                        # Add Interaction.
                        self.game.key_found = True
                        self.game_data.inc_inventory_item_by_key("keys")
                        self.render_sidebar_content(term)
                        self.render_messagebar_content(
                            term, self.game_data.get_str_in_language("entities", "key", "is_found")
                        )

    def render_layout(self, term: blessed.Terminal) -> None:
        """Render the 3 frames"""
        self._render_dict(term, self._make_border(self.scene_bounds, tuple("┌┐└┘│─")))
        self._render_dict(term, self._make_border(self.sidebar_bounds, tuple("┌┐└┘│─")))
        self._render_dict(term, self._make_border(self.message_bar_bounds, tuple("┌┐└┘│─")))

    # Render scene need to be pickup from a file
    def render_scene(self, term: blessed.Terminal):
        """Render the scene area. Design the level"""
        # Get the coordinates to be rendered in the scene panel.
        to_be_rendered = self._make_scene(self.scene_bounds, self.game.get_to_be_rendered())

        # Render the coordinates that have been added since the last frame
        self._render_dict(term, to_be_rendered - self.currently_rendered)

        # Clear the coordinates that have been removed since the last frame
        self._render_dict(term, {(i, j, " ") for i, j, _ in self.currently_rendered - to_be_rendered})

        self.currently_rendered = to_be_rendered

    def render_sidebar_content(self, term: blessed.Terminal):
        """Render the content of the sidebar. Will display all the game data"""
        start_y, end_y, start_x, end_x = self.sidebar_bounds
        panel_width = end_x - start_x
        sidebar_content = self.game.get_sidebar_content()

        # Clear the previous content in the side bar
        self._render_dict(
            term, {(i, j, " ") for i in range(start_y + 1, end_y - 1) for j in range(start_x + 1, end_x - 1)}
        )

        # Move the cursor to the top left of the sidebar
        # print(term.move_yx(start_y + 2, start_x + 2), end="", flush=True)

        x, y = start_x + 2, start_y + 2

        for data_key, data_obj in sidebar_content.items():
            if data_key == "game_data":
                print(
                    term.move_xy(x, y)
                    + getattr(term, self.colors["choice"])
                    + "Game data"
                    + " " * (panel_width - (len("Game data") + 2))
                    + getattr(term, self.term_color),
                    end="",
                )
            elif data_key == "player_data":
                # New line.
                y += 1
                print(
                    term.move_xy(x, y)
                    + getattr(term, self.colors["choice"])
                    + "In your box"
                    + " " * (panel_width - (len("In your box") + 2))
                    + getattr(term, self.term_color),
                    end="",
                )
            for key, value in data_obj.items():
                for line in chunk(f"{key} : {value}", panel_width):
                    y += 1
                    print(term.move_xy(x, y) + line, end="", flush=True)
            y += 1

        print(term.move_yx(end_y - 1, start_x + 2), end="", flush=True)
        print(getattr(term, self.colors["choice"]) + "Menu <ESC>" + getattr(term, self.term_color), end="", flush=True)

    def render_messagebar_content(self, term: blessed.Terminal, message: str = "", writing_speed: float = 0.01):
        start_y, end_y, start_x, end_x = self.message_bar_bounds
        panel_height = end_y - start_y
        panel_width = end_x - start_x

        # Clear the box before rendering any new message.
        print(term.move_xy(start_x + 4, start_y + round(panel_height / 2)), end="")
        print(" " * (panel_width - 4), end="", flush=True)
        print(term.move_left(panel_width - 4), end="")

        # Check if it can fit in first line using "chunk"?
        for letter in message:
            print(letter, end="", flush=True)
            sleep(writing_speed)

    @staticmethod
    def _make_border(bounds: Bounds, charset: tuple[str, str, str, str, str, str]) -> set[RenderableCoordinate]:
        start_i, end_i, start_j, end_j = bounds
        top_left, top_right, bottom_left, bottom_right, vertical, horizontal = charset
        return (
            # the corners:
            {
                (start_i, start_j, top_left),
                (start_i, end_j, top_right),
                (end_i, start_j, bottom_left),
                (end_i, end_j, bottom_right),
            }
            # the left and right vertical bars:
            | {(i, j, vertical) for i in range(start_i + 1, end_i) for j in (start_j, end_j)}
            # the top and bottom horizontal bars:
            | {(i, j, horizontal) for i in (start_i, end_i) for j in range(start_j + 1, end_j)}
        )

    @staticmethod
    def _make_scene(bounds: Bounds, game_map: set[RenderableCoordinate]) -> set[RenderableCoordinate]:

        scene_panel_height = bounds[1] - bounds[0]  # uppermost row - lowermost row
        scene_panel_width = bounds[3] - bounds[2]  # rightmost column - leftmost column

        clipped_map = set()

        i_coordinates = [coordinate[0] for coordinate in game_map]
        j_coordinates = [coordinate[1] for coordinate in game_map]

        scene_height = max(i_coordinates) - min(i_coordinates)
        scene_width = max(j_coordinates) - min(j_coordinates)

        for i, j, char in game_map:
            # translate from in-game coordinates to main screen coordinates
            new_i = i - scene_height // 2 + scene_panel_height // 2
            new_j = j - scene_width // 2 + scene_panel_width // 2

            # filter the coordinates which lie outside the scene panel bounds
            if _lies_within_bounds(bounds, (new_i, new_j)):
                clipped_map.add((new_i, new_j, char))

        return clipped_map

    @staticmethod
    def _render_dict(term: blessed.Terminal, data: set[RenderableCoordinate]) -> None:
        for i, j, char in data:
            print(term.move_yx(i, j) + char, end="", flush=True)
