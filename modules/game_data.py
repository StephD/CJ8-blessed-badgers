import json

# import os
# from datetime import datetime
from modules.logger import log

ASSETS_PATH = "assets"
GAMEDATA_PATH = f"{ASSETS_PATH}/gamedata.json"
GAMESAVE_NEW = f"{ASSETS_PATH}/saves/gamedata_new.json"
GAMESAVE_SAVE = f"{ASSETS_PATH}/saves/gamedata_save.json"


# class GameException(Exception):
#     """Base class for exceptions in this module."""

#     pass


class GameData:
    """Game parent class for managing the game datas"""

    def __init__(self):
        try:
            with open(GAMEDATA_PATH, "r") as file:
                self.data = json.load(file)
        except FileNotFoundError:
            pass

    def update_file_game_data(function):
        """Decorator used to save the game_data into a file when it's updated"""

        def inner(self, *args):
            function(self, *args)
            with open(GAMEDATA_PATH, "w") as file:
                json.dump(self.data, file, indent=4)

        return inner

    @update_file_game_data
    def save_game(self) -> None:
        with open(GAMESAVE_SAVE, "w") as file:
            json.dump(self.data, file, indent=4)

    @update_file_game_data
    def load_game(self, type: str = "new") -> None:
        if type == "new":
            path = GAMESAVE_NEW
        elif type == "saved":
            path = GAMESAVE_SAVE

        with open(path, "r") as file:
            data_tmp = json.load(file)
            data_tmp["game"]["language"] = self.data["game"]["language"]
            self.data = data_tmp

    @update_file_game_data
    def update_game_mode(self, game_mode):
        self.data["game"]["mode"] = game_mode

    def get_game_mode(self) -> str:
        return self.data["game"]["mode"]

    def get_language(self) -> None:
        return self.data["game"]["language"]

    @update_file_game_data
    def update_language(self, language) -> None:
        self.data["game"]["language"] = language

    def get_game_key(self, key) -> tuple[bool, str]:
        return self.data["game"][key]

    def get_inventory_items(self) -> list:
        return list(self.data["player"]["inventory"].keys())

    def get_inventory_item(self, key) -> dict:
        return self.data["player"]["inventory"][key]
