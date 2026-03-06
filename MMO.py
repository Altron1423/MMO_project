import pygame as pg
import json

from src.modules.Core import CORE

pg.init()

from src.modules.save.SaveManager import SavesManager
from src.modules.app import App
# from src.modules.Loger import loger
# loger.loging = False


class Game(App):
    save_manager:SavesManager = SavesManager()

    def __init__(self):
        super().__init__()
        # self.load_pet_feed()

        config = {
            "open_single_player": [self.open_single_player, None],
            "open_game_menu": [self.open_game_menu, None],
        }
        self.add_functions({"window": config})
        self.save_manager.set_path_save(self.path.joinpath(CORE.saves_directory))

    def load_pet_feed(self):
        with self.path.joinpath("db.json").open("r", encoding="utf-8") as file:
            self.pets = json.load(file)["pets"]

        mb = self.main_screen.window_manager.get_window("pet_feed")
        config = []
        x, y, dx, dy, sx, sy = mb.cord_new_but
        for i, ipet in enumerate(self.pets):
            pet = self.pets[ipet]
            config.append([
                "button_png",
                f"{pet['name']}, {pet['age']}",
                "run_function:app/open_pet_info",
                [
                    x + (dx + sx) * (i % 2),
                    y + (dy + sy) * (i // 2),
                    sx, sy
                ],
                "pet_feed",
                {
                    "pet_name": ipet
                },
                [
                    pet['image'][0],
                    "img_female" if pet['parameters']['gender'] == "Девочка" else "img_male"
                ]
            ])
            # log(config[-1])
        mb._menu_load({"buttons": config})

    def open_single_player(self, bat):
        wm = self.main_screen.window_manager
        self.save_manager.load_from_dir()
        wm.set_button_single(self.save_manager.get_saves_name())
        wm.set_main_window("game_select")
        wm.open_window("single_saves")

    def open_game_menu(self, bat):
        wm = self.main_screen.window_manager
        wm.set_main_window("main_menu")
        wm.close_window("single_saves")

    def gen_params(self, params):
        st_param = ["Пол:", "Порода:", "Рост:", "Вес:", "Окрас:"]
        for key, value in params.items():
            st_param.append(value)

        return st_param

    def open_pet_info(self, data):
        self.select_pet = self.pets[data.get_parameters("pet_name")]
        pet = self.select_pet
        wm = self.main_screen.window_manager
        bm = wm.get_window("head_info").button_manager
        bm._buttons[0].set_png(pet["image"][1])
        bm._buttons[0].set_text(f"{pet['name']}, {pet['age']}")

        bm = wm.get_window("detailed_information").button_manager
        bm._buttons[0].set_text(pet["descr"])
        bm._buttons[1].set_text(self.gen_params(pet["parameters"]))
        bm._buttons[2].set_text(pet["tags"])
        bm._buttons[3].set_text(["Куратор собаки:"] + pet["tutor"])

        wm.close_window("find_line")
        wm.open_window("head_info")
        wm.set_main_window("detailed_information")


if __name__ == "__main__":
    game = Game()
    game.run()
