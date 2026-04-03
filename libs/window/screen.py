from pathlib import Path

import libs.graphics.interface_elements.buttons_element as buttons
from libs import CORE
# from libs import Application
from libs.graphics.ButtonManager import ButtonManager
from libs.graphics.polygons import Resizer, Recalc
import pygame as pg
import json

from libs.Loger import loger
from libs.math import Size2, Vector2, Position2
from libs.window.Mouse import Mouse
from libs.loaders import StylerLoader, ImageLoader, ManyPolygonizerLoader


class MainScreen:
    _static_size_: bool = False
    _application: "Application"
    screen_size: Size2 = Size2()
    center_screen: Position2 = Position2()
    screenOSN: pg.Surface
    screen_main: pg.Surface
    mouse: Mouse
    window_manager: "WindowManager"
    Msize: tuple[int, int] = (1, 1)
    shift_main_screen: tuple[int, int] = (0, 0)



    def __init__(self, application: "Application"):
        self._application = application

        self.screen_size = Size2(CORE.start_size)
        self.center_screen = self.screen_size // 2

        self.screenOSN = pg.display.set_mode(self.screen_size.tuple, pg.RESIZABLE, pg.FULLSCREEN)
        self.screen_main = pg.Surface(self.screen_size.tuple)
        self.mouse = Mouse()

        self.window_manager = WindowManager(self)
        self.window_manager.resize(self.screen_size)

        loger.status("MainScreen init complete")

    def _set_start_parameters(self):
        inf = pg.display.Info()
        self.screen_size = Size2(inf.current_w, inf.current_h) // 10
        self.center_screen = self.screen_size // 2

        loger.status("Set MainScreen parameters complete")

    def draw(self):
        self.screen_main.fill((200, 200, 200))
        self.screenOSN.fill((0, 0, 0))

        self.window_manager.draw()
        self.window_blit()

    def resize_main_screen(self, new_size):
        if self._static_size_:
            loger.error("Static format not realize. Please use _static_size_ = False")
            self._static_size_ = False
            # k1 = self.screen_size[0] / self.WIDTH
            # k2 = self.screen_size[1] / self.HEIGHT
            # if k1 < k2:
            #     self.K_Mushtub = k1
            #
            #     self.shift_main_screen = (
            #         0,
            #         (self.screen_size[1] - self.HEIGHT * k1) // 2
            #     )
            # else:
            #     self.K_Mushtub = k2
            #
            #     self.shift_main_screen = (
            #         (self.screen_size[0] - self.WIDTH * k2) // 2,
            #         0
            #     )
            #
            # self.Msize = (self.WIDTH * self.K_Mushtub, self.HEIGHT * self.K_Mushtub)
            # self.mouse.update_screen_data(*self.shift_main_screen, self.K_Mushtub)
        else:
            self.screen_size = new_size
            # self.screenOSN = pg.display.set_mode(self.screen_size.tuple, pg.RESIZABLE, pg.FULLSCREEN)
            self.center_screen = self.screen_size // 2
            self.screen_main = pg.Surface(self.screen_size.tuple)
            self.window_manager.resize(self.screen_size)

    def window_blit(self):

        self.mouse.update()

        self.screenOSN.blit(self.screen_main, (0, 0))
        # screen2 = pg.transform.scale(self.screen_main, self.Msize)
        # self.screenOSN.blit(screen2, self.shift_main_screen)

        pg.display.update()


class Window(Resizer):
    first_draw_task: list[tuple[pg.Surface, tuple[int, int]]]
    second_draw_task: list[tuple[pg.Surface, tuple[int, int]]]

    def __init__(self, manager:"WindowManager", name, config, main_surface):

        surface_size = Size2(main_surface.get_size())
        super().__init__(*self._load_surface(config))
        self.surface = None
        self.background = None
        self.name = name
        self.mowing = False
        self.cord_new_but = [0] * 6

        self.cord_new_but = config["data"]["cord_new_but"]
        self.background = config["data"].get("window_background")


        self.manager = manager
        self.button_manager = ButtonManager(manager.main_screen.mouse)

        self.set_surface_size(surface_size+0)
        self.surface = pg.Surface(self.size.tuple, pg.SRCALPHA, 32)
        self.button_manager.set_surface(self.surface)

        self._menu_load(config)

        self.gen_but = []
        self.first_draw_task = []
        self.second_draw_task = []

        loger.status(f"Window '{name}' init complete whis {len(self.button_manager._buttons)}")

    @staticmethod
    def _load_surface(config:dict) -> tuple[Recalc, Recalc]:
        position = config["data"].get("window_position")
        if position is None:
            position = Recalc()
        else:
            position = Recalc.load_from_str(position)

        size = config["data"].get("window_size")
        if size is None:
            size = Recalc(Vector2(1,1))
        else:
            size = Recalc.load_from_str(size)

        return position, size

    def _menu_load(self, config):
        self.button_manager.set_address(self.name)
        data = {"shift": self.position, "scale": 1, "scaling": False}
        self.button_manager.mouse.add_address(self.name, data)


        for i_button in config["buttons"]:
            self.add_button(i_button)

    def add_task_draw(self, group: int, task: tuple[pg.Surface, tuple[int, int]]):
        if group == 1:
            self.first_draw_task.append(task)
        elif group == 2:
            self.second_draw_task.append(task)

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

    def add_button(self, button_data, last_polygons:list[str] = None) -> None:
        if last_polygons is None:
            last_polygons = [""]
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
        for i_task in self.first_draw_task:
            self.surface.blit(i_task[0], i_task[1])
        self.button_manager.draw()
        for i_task in self.second_draw_task:
            self.surface.blit(i_task[0], i_task[1])
        self.first_draw_task = []
        self.second_draw_task = []
        screen.blit(self.surface, self.position.tuple)

    def cleen_buttons(self):
        self.button_manager.cleen_buttons()

    def set_surface_size(self, surface_size: Size2):
        super().set_surface_size(surface_size)
        self.surface = pg.Surface(self.size.tuple, pg.SRCALPHA, 32)
        self.button_manager.set_surface(self.surface)


class WindowManager:
    main_screen: MainScreen
    windows: list[Window]
    windows_keys: dict[str, int]
    mainWindow: Window
    visible: list[Window]
    size: Size2

    def __init__(self, main_screen:MainScreen):
        self.main_screen = main_screen
        self.windows = []
        self.windows_keys = {}
        self.load_windows()
        self.mainWindow = self.get_window("main_menu")

        self.visible = []
        self.size = self.mainWindow.size
        # self.open_window("speed_move")
        # self.open_window("find_line")

        loger.status("WindowManager init complete")

    def load_windows(self):
        # path = self.main_screen.Application.path_map.joinpath("src/data/configs")
        path = Path.cwd().joinpath("src/data/configs")

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

    def key_press(self, key: int, key_type:int):
        self.mainWindow.button_manager.key_press(key, key_type)
        if key == pg.K_F11 and key_type == pg.KEYUP:
            # print(pg.display.is_fullscreen())
            pg.display.toggle_fullscreen()
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
        result = self.main_screen._application.give_function(data)
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
                "button", buttons[i_button], "run_function:window/save_select",
                [f"<Recalc:<Vector2:0,0>/<Vector2:{100},{25 + i_button * 100}>>", f"<Recalc:<Vector2:0,0>/<Vector2:{400},{75}>>"],
                "interface", None, None
            ])
        window.set_surface_size(self.size)


    def resize(self, size: Size2):
        self.size = size
        for window in self.windows:
            window.set_surface_size(size)
    # def set_button_single(self, save_names: list[str]):
    #     self.get_window("single_saves").cleen_buttons()
    #     self._append_buttons(save_names, "single_saves")
