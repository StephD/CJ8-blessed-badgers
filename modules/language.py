import json

GAMEDATA_PATH = "assets/gamedata.json"
LANGUAGE_PATH = "assets/lang/"


class Language:
    """
    This module will be use to define function to get the language, text, message from the file

    It need to define a get method for the good language
    Language are pick in a CSV
    """

    def __init__(self) -> None:
        self.game_language = self.get_language()

    # Code edited by FamethystForLife
    def get(self, *args) -> str:
        selections = [*args]

        # Parse appropriate JSON language file based on lang param
        with open(LANGUAGE_PATH + f"lang_{self.game_language}.json", "r") as lang:
            lang_dict = json.load(lang)

        # Obtain appropriate string
        for key in selections:
            lang_dict = lang_dict[key]

        return lang_dict

    def set_language(self) -> None:
        pass

    def get_language(self) -> str:
        with open(GAMEDATA_PATH, "r") as file:
            db = json.load(file)
        return db["game"]["language"].lower()

    def get_text(self, text_category, text_command) -> str:
        #
        pass
