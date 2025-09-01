import pygame as pg
# import data.base as base
pg.init()
import data.screen as screen
import server
import json
import data.world as world


class Game:
    def __init__(self):
        self.server = server.Server()
        self.clock = pg.time.Clock()
        self.TPS = 20
        self.tick = 0
        self.main_screen = screen.MainScreen(self)
        self.WORK = True
        with open(f"data/core.json", "r", encoding="utf-8") as f:
            self.core = json.load(f)
        self.version = list(map(int, self.core["version"].split(".")))
        self.seves = world.Saves(self)
        self.function_rans = {"sistem": {"exit": [self.exit, None]}, "mods": {}}

    def run(self):
        while self.WORK:
            self.tick += 1
            self.clock.tick(self.TPS)
            self.main_screen.draw()

    def exit(self):
        self.WORK = False

    def start_server(self):
        self.server.start()
        self.world = world.Worlds()

    def detect_saves(self):
        a = self.seves.detect_saves([0,1,0])
        print(a)

    def give_function(self, data, passw=None):
        m = self.function_rans
        for i in data:
            if i in m:
                m = m[i]
            else:
                return {"result": False, "error": [0, f"{i} from {data} undefined"]}
        if type(m) == dict:
            return {"result": False, "error": [1, f"{data} is unfull address"]}
        elif m[1] == passw:
            return {"result": True, "function": m[0]}
        else:
            return {"result": False, "error": [3, f"uncorrect passw"]}





if __name__ == "__main__":
    game = Game()
    game.run()

