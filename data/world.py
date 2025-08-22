# import base
import os
import json

# class Worlds(base.GameElement):
class Saves:
    class Save:
        def __init__(self, path):
            self.path = path
            with open(f"{path}\\main.json", "r", encoding="utf-8") as f:
                self.data = json.load(f)
            self.version = list(map(int, self.data["version"].split(".")))
            self.options = {}

        def load(self):
            with open(f"{self.path}\\options.json", "r", encoding="utf-8") as f:
                self.options = json.load(f)

        def __str__(self):
            return str(self.__dict__)


    def __init__(self, game):
        self.game = game
        self.saves_path = os.getcwd().replace(r"\data", r"\saves", 1)
        self.saves = []

    def detect_saves(self, version):
        self.saves = []
        for i in os.listdir(self.saves_path):
            save = self.Save(f"{self.saves_path}\\{i}")
            if save.version <= version:
                self.saves.append(save)
        return self.saves


class Worlds():
    def __init__(self):
        # super(Worlds, self).__init__(f"saves/test_world/options.json", [])
        pass


class WorldBlock:
    def __init__(self):
        # self.size_x = 50
        # self.size_y = 50
        pass

if __name__ == '__main__':
    world = Worlds()
    # world.save()
    s = Saves("")
    print(s.detect_saves([0,1,0]))
