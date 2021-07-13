import json
import os
from datetime import datetime

# TODO


class Datastore:
    def __init__(self, save_name):
        self.save_name = save_name
        self.create_game()

    def create_game(self) -> None:
        """Creates or load a game"""
        # Create game if not exist
        if not os.path.isfile(f"./assets/saves/{self.save_name}.json"):
            base_save = {
                "game": {
                    "is_game_already_played": False,
                    "game_mode": "game/tutorial",
                    "language": "EN",
                    "last_saved": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                },
                "room": {},
                "player": {"lifes_left": 3, "current_room": 1, "last_position": [0, 0], "inventory": {}},
            }
            with open(f"./assets/saves/{self.save_name}.json", "w+") as f:
                json.dump(base_save, f, indent=4)
            self.data = base_save
        else:
            with open(f"./assets/saves/{self.save_name}.json", "r+") as f:
                self.data = json.load(f)

    def save_game(self) -> None:
        """Save game data back into JSON file"""
        with open(f"./assets/saves/{self.save_name}.json", "w+") as f:
            json.dump(self.data, f, indent=4)

    def update_lang(self, lang) -> None:
        self.data["game"]["language"] = lang
        self.save_game()

    def update_game_attr(self, game, key, value) -> None:
        self.data["game"][key] = value
        self.save_game()

    def add_room(self, room_id) -> None:
        """Adds a room to the game"""
        base_room = {
            "is_door_unlock": False,
            "is_key_is_found": False,
            "is_secret_door_found": False,
            "items": {},
            "interactions": {},
        }
        self.data["room"][room_id] = base_room
        self.save_game()

    def add_item_to_room(self, room_id, item_name, item_pos) -> None:
        self.data["room"][room_id]["items"] = {item_name: {"last_pos": item_pos}}
        self.save_game()

    def add_interactive_to_room(self, room_id, interaction_name) -> None:
        self.data["room"][room_id]["interactions"] = {interaction_name: False}
        self.save_game()

    def update_room_attr(self, room_id, key, value) -> None:
        self.data["room"][room_id][key] = value
        self.save_game()

    def update_room_item(self, room_id, item, last_pos) -> None:
        self.data["room"][room_id]["items"][item] = {"last_pos": last_pos}
        self.save_game()

    def update_room_interactive(self, room_id, interactive, value) -> None:
        self.data["room"][room_id]["interactions"][interactive] = value
        self.save_game()

    def update_player_attr(self, key, value) -> None:
        self.data["player"][key] = value
        self.save_game()

    def update_inventory(self, action, item, room_id=None, quantity=None) -> None:
        if action == "del":
            del self.data["player"]["inventory"][item]
            self.save_game()
        elif action == "add":
            self.data["player"]["inventory"] = {item: {"origin": room_id, "quantity": quantity}}
            self.save_game()
        else:
            pass

    def get_game(self, key) -> tuple[bool, str]:
        return self.data["game"][key]

    def get_room(self, room_id, type, key) -> tuple[bool, str, dict]:
        if type == "base":
            return self.data["room"][room_id][key]
        elif type == "item":
            return self.data["room"][room_id]["items"][key]
        elif type == "interactive":
            return self.data["room"][room_id]["interactions"][key]

    def get_player(self, key) -> tuple[int, list, dict]:
        return self.data["player"][key]

    def get_inventory_list(self) -> list:
        return list(self.data["player"]["inventory"].keys())

    def get_inventory_item(self, key) -> dict:
        return self.data["player"]["inventory"][key]
