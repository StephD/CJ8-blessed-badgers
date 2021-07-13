import json

from modules.game_data import GameData

LANGUAGE_PATH = "assets/lang/"


class Language:
    """
    This module will be use to define function to get the language, text, message from the file

    It need to define a get method for the good language
    Language are pick in a CSV
    """

    def __init__(self, language: str = "en") -> None:
        self.game_language = language

    def get_str_in_language(self, *args) -> str:
        selections = [*args]

        with open(LANGUAGE_PATH + f"lang_{self.game_language}.json", "r", encoding="utf-8") as lang:
            lang_dict = json.load(lang)

        for key in selections:
            lang_dict = lang_dict[key]

        return lang_dict
