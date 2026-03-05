import pygame as pg

# import data.base as base
pg.init()
from pathlib import Path
from __dop.src2.data.Loger import log, status, log_step
import data.screen as screen
import data.GameSession as GameSession
import json


class Game:
    def __init__(self):
        status("Game init started")

        self._set_start_parameters()

        self.gameSession = GameSession.GameSession(self)

        self.main_screen = screen.MainScreen(self)

        self._create_functions_dict()

        status("Game init complete")
        log_step(2)


    def run(self):
        status("Game start")
        while self.WORK:
            self.tick += 1
            self.clock.tick(self.TPS)
            self.main_screen.draw()

    def exit(self):
        self.WORK = False
        log("Game exit")

    def _set_start_parameters(self):
        self.clock = pg.time.Clock()
        self.TPS = 20
        self.tick = 0
        self.path = Path.cwd()
        self.WORK = True

        with self.path.joinpath(f"data/core.json").open("r") as f:
            self.core = json.load(f)
        self.version = list(map(int, self.core["version"].split(".")))

        status(f"Game version: {self.version}")
        status("Set Game parameters complete")

    def _create_functions_dict(self):
        sist = {
            "exit": [self.exit, None],
            "single_saves": [self.open_single_saves, None]
        }
        self.function_rans = {"sistem": sist, "mods": {}}

        status("Function giver generate complete")

    def give_function(self, data, passw=None):
        m: dict | list = self.function_rans
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

    def open_single_saves(self):
        self.gameSession.open_single_saves()
        self.main_screen.window_manager.set_main_window("single_saves")



if __name__ == "__main__":
    game = Game()
    game.run()
