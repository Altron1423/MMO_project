import __dop.src2.graphics.old_buttons as buttons
import pygame as pg
import json

from __dop.src2.data.Loger import status, log
from __dop.src2.data.Mouse import Mouse


class MainScreen:
    def __init__(self, game):
        self.GAME = game
        self._set_start_parameters()
        self.screenOSN = pg.display.set_mode(self.screenSize, pg.RESIZABLE)
        self.screen_main = pg.Surface(self.screenSize)
        self.menu = buttons.Menu()
        self.window_manager = WindowManager(self)
        self.mouse = Mouse(pg.mouse)

        status("MainScreen init complete")

    def _set_start_parameters(self):
        self.screenSize = self.WIDTH, self.HEIGHT = 800, 900
        self.centr = self.H_WIDTH, self.H_HEIGHT = self.WIDTH // 2, self.HEIGHT // 2
        self.K_Mushtub = 1
        self.shift_main_screen = (0, 0)
        self.Msize = self.screenSize

        status("Set MainScreen parameters complete")

    def draw(self):
        self.screen_main.fill((200, 200, 200))
        self.screenOSN.fill((0, 0, 0))

        for event in pg.event.get():
            # print(event.type, pg.MOUSEBUTTONUP, pg.MOUSEBUTTONDOWN)
            if event.type == pg.QUIT:
                self.GAME.exit()
            elif event.type == pg.KEYDOWN or event.type == pg.KEYUP:
                self.window_manager.keyPress(event.key, event.type)
                # self.menu.keyPress(event.key, event.type)
            elif event.type == pg.MOUSEBUTTONDOWN or event.type == pg.MOUSEBUTTONUP:
                self.window_manager.select(event.button, event.type)
            elif event.type == pg.VIDEORESIZE:
                self.resize_main_screen(event.size)

        self.window_manager.draw()
        # self.menu.draw(self.screen, self.mousePos)
        self.window_blit()

    def resize_main_screen(self, new_size):
        self.screenSize = new_size
        k1 = self.screenSize[0] / self.WIDTH
        k2 = self.screenSize[1] / self.HEIGHT
        if k1 < k2:
            self.K_Mushtub = k1

            self.shift_main_screen = (
                0,
                (self.screenSize[1] - self.HEIGHT * k1) // 2
            )
        else:
            self.K_Mushtub = k2

            self.shift_main_screen = (
                (self.screenSize[0] - self.WIDTH * k2) // 2,
                0
            )

        self.Msize = (self.WIDTH * self.K_Mushtub, self.HEIGHT * self.K_Mushtub)
        self.mouse.update_screen_data(*self.shift_main_screen, self.K_Mushtub)


    def window_blit(self):

        self.mouse.update()

        screen2 = pg.transform.scale(self.screen_main, self.Msize)
        self.screenOSN.blit(screen2, self.shift_main_screen)

        pg.display.update()

    def append_single_saves(self, buttons:list):
        self.window_manager._append_buttons(buttons, "single_saves")

    def append_online_saves(self, buttons:list):
        self.window_manager._append_buttons(buttons, "online_saves")


class WindowManager:
    def __init__(self, main_screen):
        self.main_screen = main_screen
        firs_style = buttons.ColorT((40, 250, 250))
        firs_style.append("buttonFonAc", {"rgb": (250, 250, 40)})
        self.styles = {"error_style": firs_style}
        self.windows = []
        self.windows_keys = {}
        self.load_windows()
        self.mainWindow = self.windows[0]

        status("WindowManager init complete")

    def load_windows(self):
        path = self.main_screen.GAME.path
        with path.joinpath("data/styles_config.json").open("r", encoding="utf-8") as f:
            styles_config = json.load(f)

        for i_style in styles_config:
            style_struct = styles_config[i_style]
            style = buttons.ColorT(style_struct[0])
            for i in style_struct[1]:
                style.append(i, style_struct[1][i])
            self.styles[i_style] = style


        with path.joinpath("data/buttons_config.json").open("r", encoding="utf-8") as f:
            buttons_config = json.load(f)

        for window in buttons_config:
            self.windows.append(Window(self, window, buttons_config[window]))
            self.windows_keys[window] = len(self.windows) - 1

        status(f"Load {len(self.windows)} windows")

    def draw(self):
        # log(self.main_screen.mouse.get_position())
        self.mainWindow.menu.draw(self.main_screen.screen_main, self.main_screen.mouse.get_position())

    def keyPress(self, key, type):
        self.mainWindow.menu.keyPress(key, type)
        pass

    def select(self, button, type):
        self.mainWindow.menu.select(button, type)
        pass

    def genegate_function(self, data):
        data = data.split(":")
        if data[0] == "move_window":
            return lambda x: self.set_main_window(data[1])
        elif data[0] == "run_function":
            return lambda x: self.run_function(data[1])

    def set_main_window(self, window):
        # print(window)
        self.mainWindow = self.windows[self.windows_keys[window]]
        log(f"Move to '{window}' window")

    def run_function(self, data):
        data = data.split("/")
        result = self.main_screen.GAME.give_function(data)
        if result["result"]:
            result["function"]()
        else:
            print(result["error"])

    def get_style(self, style_name):
        if style_name in self.styles:
            return self.styles[style_name]
        print(f"ERROR:   WindowManager::get_style - unknown style: {style_name}")
        return self.styles["error_style"]

    def _append_buttons(self, buttons, screen:str):
        window = self.windows[self.windows_keys[screen]]
        for i in range(len(buttons)):
            window.add_button(buttons[i])


class Window:
    def __init__(self, manager:WindowManager, name, config):
        self.manager = manager
        self.name = name
        self.mowing = False
        self.menu = buttons.Menu()
        self.cord_new_but = [0] * 6
        self.default_style = None
        self.menu_load(config)

        self.gen_but = []

        status(f"Window '{name}' init complete")

    def menu_load(self, config):
        # game = self.manager.game
        # print(config)
        self.cord_new_but = config["data"]["cord_new_but"]
        self.default_style = self.manager.get_style(config["data"]["default_style"])
        for i_button in config["buttons"]:
            if i_button[0] == "button":
                # print("  ", i_button, i_button[2])
                f = self.manager.genegate_function(i_button[2])

                self.menu.append_option(i_button[1], f, i_button[3], self.manager.get_style(i_button[4]))


    def move_new_button(self):
        n = len(self.gen_but)

        # x0, y0 = 100, 170
        #
        # dx, dy = 0, 70
        #
        # sx, sy = 100, 50
        x0, y0, dx, dy, sx, sy = self.cord_new_but

        if dx == None:
            dx = -sx
        if dy == None:
            dy = -sy

        return x0 + (dx + sx) * n, y0 + (dy + sy) * n, sx, sy

    def add_button(self, data):
        l = lambda but: print(f"select {but.description}")
        self.gen_but.append(
            self.menu.append_option(data[0], l, self.move_new_button(), self.default_style, descr=data[0])
        )
