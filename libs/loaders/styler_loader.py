from libs.graphics.styler import Styler
from pathlib import Path
import json

if __name__ == '__main__':
    import pygame as pg
    pg.init()

class StylerLoader:
    def __init__(self):
        self.styles = {}

    def load_styles(self, path):
        with Path(path).open("r", encoding="utf-8") as file:
            json_data = json.load(file)
            if json_data["type"] == "styler":
                json_data = json_data["styles"]
                for name in json_data:
                    style = Styler.load_json(json_data[name])
                    self.add_style(style, name)

    def add_style(self, style, name):
        self.styles[name] = style

    def get_styler(self, name):
        return self.styles[name]



styler_loader = StylerLoader()
if __name__ == "__main__":
    path = Path(r"C:\Users\Altron\PycharmProjects\MMO_project\src\data\configs\styles_config.json")
    styler_loader.load_styles(path)
