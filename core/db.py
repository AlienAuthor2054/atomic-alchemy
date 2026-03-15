import json
import os

class Database():
    def __init__(self):
        self.options_path = "data/options.json"
        self.lb_path = "data/leaderboard.json"

        if not os.path.isdir('data'):
            os.mkdir('data')

    def get_options(self):
        try:
            with open(file=self.options_path, mode="r") as file:
                data = json.load(file)

                return data
            
        except FileNotFoundError as error:
            with open(file=self.options_path, mode="w") as file:
                data = {
                    "volume_music": 50,
                    "volume_sfx": 50
                }

                json.dump(data, file, indent=4)

            return self.get_options()

    def set_options(self, data):
        with open(file=self.options_path, mode="w") as file:
            json.dump(data, file, indent=4)

    def get_lb(self):
        try:
            with open(file=self.lb_path, mode="r") as file:
                data = json.load(file)

                return data
            
        except FileNotFoundError as error:
            with open(file=self.lb_path, mode="w") as file:
                data = {
                    "leaderboard": []
                }

                json.dump(data, file, indent=4)

            return self.get_lb()

    def set_lb(self, data):
        with open(file=self.lb_path, mode="w") as file:
            json.dump(data, file, indent=4)

