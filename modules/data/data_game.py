from modules.game_data import GameData, save_game


class DataGame(GameData):
    def read_language(self) -> None:
        return self.data["game"]["language"]

    @save_game
    def update_language(self, lang) -> None:
        self.data["game"]["language"] = lang
