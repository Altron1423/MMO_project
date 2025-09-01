import graphics.buttons as buttons
import pygame as pg
import json

class MainScreen:
    def __init__(self, game):
        self.GAME = game
        self.screenSize = self.WIDTH, self.HEIGHT = 800, 900
        self.centr = self.H_WIDTH, self.H_HEIGHT = self.WIDTH // 2, self.HEIGHT // 2
        self.K_Mushtub = 1
        self.centrovka = True
        self.screenOSN = pg.display.set_mode(self.screenSize, pg.RESIZABLE)
        self.screen = pg.Surface(self.screenSize)
        self.menu = buttons.Menu()
        self.window_manager = WindowManager(self)
        self.mousePos = (-1, -1)

    def draw(self):
        self.screen.fill((200, 200, 200))
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
                self.screenSize = event.size
                k1 = self.screenSize[0] / self.WIDTH
                k2 = self.screenSize[1] / self.HEIGHT
                if k1 < k2:
                    self.K_Mushtub = k1
                    self.centrovka = True
                else:
                    self.K_Mushtub = k2
                    self.centrovka = False


        self.window_manager.draw()
        # self.menu.draw(self.screen, self.mousePos)


        if self.centrovka:
            dx = 0
            dy = (self.screenSize[1] - self.HEIGHT * self.K_Mushtub) // 2
        else:
            dx = (self.screenSize[0] - self.WIDTH * self.K_Mushtub) // 2
            dy = 0

        self.mousePos2 = ((self.mousePos[0] - dx) // self.K_Mushtub, (self.mousePos[1] - dy) // self.K_Mushtub)
        screen2 = pg.transform.scale(self.screen, (self.WIDTH * self.K_Mushtub, self.HEIGHT * self.K_Mushtub))
        self.screenOSN.blit(screen2, (dx, dy))
        if pg.mouse.get_focused():
            self.mousePos = pg.mouse.get_pos()
        else:
            self.mousePos = (-1, -1)

        pg.display.update()


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

    def load_windows(self):
        with open(r"data\styles_config.json", "r", encoding="utf-8") as f:
            styles_config = json.load(f)

        for i_style in styles_config:
            style_struct = styles_config[i_style]
            style = buttons.ColorT(style_struct[0])
            for i in style_struct[1]:
                style.append(i, style_struct[1][i])
            self.styles[i_style] = style


        with open(r"data\buttons_config.json", "r", encoding="utf-8") as f:
            buttons_config = json.load(f)

        for window in buttons_config:
            self.windows.append(Window(self, window, buttons_config[window]))
            self.windows_keys[window] = len(self.windows) - 1

    def draw(self):
        self.mainWindow.menu.draw(self.main_screen.screen, self.main_screen.mousePos)

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


class Window:
    def __init__(self, manager:WindowManager, name, config):
        self.manager = manager
        self.name = name
        self.mowing = False
        self.menu = buttons.Menu()
        self.menu_load(config)

    def menu_load(self, config):
        # game = self.manager.game
        # print(config)
        for i_button in config:
            if i_button[0] == "button":
                # print("  ", i_button, i_button[2])
                f = self.manager.genegate_function(i_button[2])

                self.menu.append_option(i_button[1], f, i_button[3], self.manager.get_style(i_button[4]))

