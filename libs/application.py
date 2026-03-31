from typing import Callable

import pygame as pg

from pathlib import Path
from libs.Core import CORE
from libs.Loger import loger
import src.modules.screen as screen
from libs.ticker import Ticker


class Application:
    clock: pg.time.Clock
    TPS: int
    tick: Ticker
    path: Path
    WORK: bool
    main_screen: screen.MainScreen
    function_runs: dict[str, dict[str, list[Callable[..., None] | None]]]

    def __init__(self):
        loger.status("App init started")

        self._set_start_parameters()

        self.main_screen = screen.MainScreen(self)

        self._create_functions_dict()


        loger.status("App init complete")
        loger.pass_line(2)

    def run(self):
        loger.status("App start")
        try:
            while self.WORK:
                self.tick.tick()
                self.clock.tick(self.TPS)

                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        self.exit(None)
                    elif event.type == pg.KEYDOWN or event.type == pg.KEYUP:
                        self.main_screen.window_manager.keyPress(event.key, event.type)
                        self.key_press(event.key, event.type == pg.KEYDOWN)
                    elif event.type == pg.MOUSEBUTTONDOWN or event.type == pg.MOUSEBUTTONUP:
                        self.main_screen.window_manager.select(event)
                    elif event.type == pg.VIDEORESIZE:
                        self.main_screen.resize_main_screen(event.size)

                self.main_screen.draw()
                self.run_more()
        except KeyboardInterrupt:
            self.exit()

    def key_press(self, key: str, key_down: bool):
        ...

    def run_more(self):
        ...

    def exit(self, _=None):
        self.WORK = False
        loger.log("App exit")

    def _set_start_parameters(self):
        self.clock = pg.time.Clock()
        self.TPS = 20
        self.tick = Ticker()
        self.path = Path.cwd()
        self.WORK = True

        loger.status(f"App version: {CORE.version}")
        loger.status("Set App parameters complete")

    def _create_functions_dict(self):
        sist = {
            "exit": [self.exit, None]
        }
        self.function_runs = {"sistem": sist, "mods": {}}

        loger.status("Function giver generate complete")

    def add_functions(self, dict_functions: dict):
        """
        {"key": {"name": [lambda x: print(1), None]}}
        :param dict_functions:
        :return:
        """
        for key, functions in dict_functions.items():
            if key != "sistem":
                if key not in self.function_runs:
                    self.function_runs[key] = {}
                for name, function in functions.items():
                    self.function_runs[key][name] = function

    def give_function(self, data, passw=None):
        m: dict | list = self.function_runs
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



