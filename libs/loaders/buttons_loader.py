from pathlib import Path
from src import log
import json

from src import ButtonManager


class ButtonManagerLoader:
    def __init__(self):
        self.buttons = {}

    def add_menu(self, menu, name):
        self.buttons[name] = menu

    def load_images(self, path):
        with Path(path).open("r", encoding="utf-8") as file:
            json_data = json.load(file)
            if json_data["type"] == "interface_elements":
                json_data = json_data["windows"]
                button_manager = ButtonManager(None)

                # for name in json_data:
                #     menu = [None, json_data[name]]
                #     self.add_menu(menu, name)

