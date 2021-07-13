import json

# import os
# from datetime import datetime

GAMEDATA_PATH = "assets"
GAMESAVE_NAME = "gamedata_save"


def save_game(function) -> None:
    """Save game data back into JSON file"""

    def inner(self, *args):
        ret = function(self, *args)
        with open(f"{GAMEDATA_PATH}/saves/{GAMESAVE_NAME}.json", "w+") as file:
            json.dump(self.data, file, indent=4)
        return ret

    return inner()


class GameException(Exception):
    """Base class for exceptions in this module."""

    pass


class GameData:
    """Game parent class for managing the game datas"""

    def __init__(self):
        try:
            with open(f"{GAMEDATA_PATH}/gamedata.json", "r+") as file:
                self.data = json.load(file)
        except FileNotFoundError:
            pass

    def get_data(self):
        return self.data
