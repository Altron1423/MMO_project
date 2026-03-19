import libs.graphics.interface_elements.buttons_element as buttons
from libs.graphics.ButtonManager import ButtonManager
from libs.graphics.polygons import Resizer
import pygame as pg
import json

from libs.Loger import loger
from libs.window.Mouse import Mouse
from libs.loaders import StylerLoader, ImageLoader, ManyPolygonizerLoader


class MainScreen:
    def __init__(self, application):
        self.Application = application
        self._set_start_parameters()
        self.screenOSN = pg.display.set_mode(self.screenSize, pg.RESIZABLE)
        self.screen_main = pg.Surface(self.screenSize)
        self.mouse = Mouse(pg.mouse)
        # self.menu = interface_elements.ButtonManager()
        self.window_manager:WindowManager = WindowManager(self)

        loger.status("MainScreen init complete")

    def _set_start_parameters(self):
        self.screenSize = self.WIDTH, self.HEIGHT = 800, 900
        self.centr = self.H_WIDTH, self.H_HEIGHT = self.WIDTH // 2, self.HEIGHT // 2
        self.K_Mushtub = 1
        self.shift_main_screen = (0, 0)
        self.Msize = self.screenSize

        loger.status("Set MainScreen parameters complete")

    def draw(self):
        self.screen_main.fill((200, 200, 200))
        self.screenOSN.fill((0, 0, 0))

        for event in pg.event.get():
            # print(event.type, pg.MOUSEBUTTONUP, pg.MOUSEBUTTONDOWN)
            if event.type == pg.QUIT:
                self.Application.exit(None)
            elif event.type == pg.KEYDOWN or event.type == pg.KEYUP:
                self.window_manager.keyPress(event.key, event.type)
                # self.menu.keyPress(event.key, event.type)
            elif event.type == pg.MOUSEBUTTONDOWN or event.type == pg.MOUSEBUTTONUP:
                self.window_manager.select(event)
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


class Window(Resizer):
    def __init__(self, manager:"WindowManager", name, config, main_surface):
        self.surface = None
        self.background = None
        self.manager = manager
        self.name = name
        self.mowing = False
        self.button_manager = ButtonManager(manager.main_screen.mouse)
        self.cord_new_but = [0] * 6

        self.cord_new_but = config["data"]["cord_new_but"]
        self.background = config["data"].get("window_background")


        self._load_surface(config, main_surface)
        self._menu_load(config)

        self.gen_but = []

        loger.status(f"Window '{name}' init complete whis {len(self.button_manager._buttons)}")

    def _load_surface(self, config:dict, main_surface):

        position = config["data"].get("window_position", [0, 0])
        size = config["data"].get("window_size", main_surface.get_size())
        super().__init__(position, size)

        self.set_surface_size(main_surface.get_size())

        position = config["data"].get("window_percent_position")
        if position is not None:
            self.set_percent_position(*position)

        size = config["data"].get("window_percent_size")
        if size is not None:
            self.set_percent_size(*size)

        self.surface = pg.Surface(self.size, pg.SRCALPHA, 32)
        self.button_manager.set_surface(self.surface)

    def _menu_load(self, config):
        self.button_manager.set_address(self.name)
        data = {"shift": self.position, "scale": 1, "scaling": False}
        self.button_manager.mouse.add_address(self.name, data)


        for i_button in config["buttons"]:
            self.add_button(i_button)

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

    def add_button(self, button_data, last_polygons=[""]) -> None:
        if button_data[2] != last_polygons[0]:
            polygons = ManyPolygonizerLoader.get_polygonizer(button_data[4])
            self.button_manager.set_polygonizer(polygons)
            # last_polygons[0] = button_data[2]

        if button_data[0] == "button":
            button = self.button_manager.add_button(button_data[1], button_data[3], None)
            trigger = self.manager.generate_function(button_data[2], button)
            button.set_triggers(trigger)
        elif button_data[0] == "button_png":
            button = self.button_manager.add_png_but(button_data[3], None, button_data[6])
            trigger = self.manager.generate_function(button_data[2], button)
            button.set_triggers(trigger)
            button.set_text(button_data[1])
        elif button_data[0] == "png":
            button = self.button_manager.add_png(button_data[3], button_data[6])
            button.set_text(button_data[1])
        elif button_data[0] == "txt":
            button = self.button_manager.add_text(button_data[1], button_data[3])
        else:
            return

        # loger.log(button_data)

        if button_data[5] is not None:
            for key, value in button_data[5].items():
                button.set_parameters(key, value)

        # loger.log(button)

        if button_data[5] is not None:
            for key, value in button_data[5].items():
                button.set_parameters(key, value)

    def draw(self, screen):
        if self.background is not None:
            self.surface.fill(self.background)
        self.button_manager.draw()
        screen.blit(self.surface, self.position)

    def cleen_buttons(self):
        self.button_manager.cleen_buttons()

class WindowManager:
    main_screen: MainScreen
    windows: list[Window]
    windows_keys: dict[str: Window]
    mainWindow: Window
    visible: list[Window]

    def __init__(self, main_screen:MainScreen):
        self.main_screen = main_screen
        self.windows = []
        self.windows_keys = {}
        self.load_windows()
        self.mainWindow = self.get_window("main_menu")

        self.visible = []
        # self.open_window("speed_move")
        # self.open_window("find_line")

        loger.status("WindowManager init complete")

    def load_windows(self):
        path = self.main_screen.Application.path.joinpath("src/data/configs")

        loger.log(path)

        StylerLoader.load_styles(path.joinpath("styles_config.json"))

        ImageLoader.load_images(path.joinpath("images_config.json"))

        ManyPolygonizerLoader.load_manyPolygonizers(path.joinpath("many_polygon_config.json"))



        with path.joinpath("buttons_config.json").open("r", encoding="utf-8") as f:
            buttons_config = json.load(f)

        loger.log(buttons_config)

        if buttons_config["type"] == "interface_elements":
            buttons_config = buttons_config["windows"]
            for window in buttons_config:
                self.windows.append(Window(self, window, buttons_config[window], self.main_screen.screen_main))
                self.windows_keys[window] = len(self.windows) - 1


        loger.status(f"Load {len(self.windows)} windows")

    def get_window(self, name):
        return self.windows[self.windows_keys[name]]

    def draw(self):
        # loger.log(self.main_screen.mouse.get_position())
        # self.mainWindow.button_manager.draw()
        self.mainWindow.draw(self.main_screen.screen_main)
        for window in self.visible:
            window.draw(self.main_screen.screen_main)

    def keyPress(self, key, type):
        # self.mainWindow.button_manager.keyPress(key, type)
        pass

    def select(self, button):
        self.mainWindow.button_manager.select(button)
        for window in self.visible:
            window.button_manager.select(button)

    def generate_function(self, data, button) -> buttons.TriggerGen:
        data = data.split(":")
        trigger = buttons.TriggerGen()
        if data[0] == "move_window":
            trigger.LMU(lambda x: self.set_main_window(data[1]))
        elif data[0] == "run_function":
            trigger.LMU(lambda x: self.run_function(data[1], button))
        return trigger

    def set_main_window(self, window):
        # print(window)
        self.mainWindow = self.windows[self.windows_keys[window]]
        loger.log(f"Move to '{window}' window")

    def run_function(self, data, button):
        data = data.split("/")
        result = self.main_screen.Application.give_function(data)
        if result["result"]:
            result["function"](button)
        else:
            print(result["error"])

    def close_window(self, window=None):
        if window is None:
            self.visible = []
        else:
            win = self.get_window(window)
            if win is not None:
                if win in self.visible:
                    self.visible.remove(win)

    def open_window(self, window):
        self.visible.append(self.windows[self.windows_keys[window]])

    def _append_buttons(self, buttons: list[str], screen:str):
        window = self.get_window(screen)
        for i_button in range(len(buttons)):
            window.add_button([
                "button", buttons[i_button], "run_function:test/test_function",
                [100, 25 + i_button * 100, 400, 75], "interface", None, None
            ])

    # def set_button_single(self, save_names: list[str]):
    #     self.get_window("single_saves").cleen_buttons()
    #     self._append_buttons(save_names, "single_saves")
