from json import JSONDecodeError

from ursina import Vec3
import json
import os

game_save_data = {
    "player_position": [0, 0, 0]
}

def save_game_data(player):
    with open("../save_file.json", "w") as f:
        game_save_data["player_position"] = list(player.position)

        json.dump(game_save_data, f)

def get_game_data(player):
    with open("../save_file.json", "r") as f:
        data = json.load(f)

def load_game_data(player):
    has_save_file = os.path.exists("../save_file.json")

    if has_save_file:
        with open("../save_file.json", "r") as file:
            try:
                data = json.load(file)
            except JSONDecodeError as e:
                print("Couldn't load data: " + str(e))
                return

            if data["player_position"]:
                player.position = Vec3(data["player_position"][0], data["player_position"][1], data["player_position"][2])
    else:
        with open('../save_file.json', 'w') as file:
            json.dump(game_save_data, file)
