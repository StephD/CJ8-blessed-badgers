import json


class Language:
    """
    This module will be use to define function to get the language, text, message from the file

    It need to define a get method for the good language
    Language are pick in a CSV
    """

    def __init__(self) -> None:
        self.user_language = "EN"
        # pass

    # Code edited by FamethystForLife
    def get(self, *args) -> str:
        selections = [*args]

        # Parse appropriate JSON language file based on lang param
        file_template = "../assets/lang/lang_{}.json"
        copy = self.language
        selected_lang_path = file_template.format(copy.lower())
        with open(selected_lang_path, "r") as lang:
            lang_dict = json.load(lang)

        # Obtain appropriate string
        for key in selections:
            lang_dict = lang_dict[key]

        return lang_dict

    def set_language(self) -> None:
        pass

    def get_language(self) -> str:
        pass

    def get_text(self, text_category, text_command) -> str:
        #
        pass
