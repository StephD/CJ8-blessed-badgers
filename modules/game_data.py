import json

# import os
# from datetime import datetime
from modules.logger import log

GAMEDATA_PATH = "assets"
GAMESAVE_NAME = "gamedata_save"


# class GameException(Exception):
#     """Base class for exceptions in this module."""

#     pass


class GameData:
    """Game parent class for managing the game datas"""

    def __init__(self):
        try:
            with open(f"{GAMEDATA_PATH}/gamedata.json", "r+") as file:
                self.data = json.load(file)
        except FileNotFoundError:
            pass

    def update_file_game_data(function):
        """Save game data back into JSON file"""

        def inner(self, *args):
            function(self, *args)
            with open(f"{GAMEDATA_PATH}/gamedata.json", "w+") as file:
                json.dump(self.data, file, indent=4)

        return inner

    def get_language(self) -> None:
        return self.data["game"]["language"]

    @update_file_game_data
    def update_language(self, language) -> None:
        self.data["game"]["language"] = language
