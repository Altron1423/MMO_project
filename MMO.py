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



if __name__ == "__main__":
    game = Game()
    game.run()

