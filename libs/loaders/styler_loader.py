from libs.graphics.styler import Styler
from pathlib import Path
import json

from libs.loaders.loader import Loader

if __name__ == '__main__':
    import pygame as pg
    pg.init()

class StylerLoader(Loader):
    elements: dict[str, Styler]

    def load(self, path: Path):
        with path.open("r", encoding="utf-8") as file:
            json_data = json.load(file)
            if json_data["type"] == "styler":
                json_data = json_data["styles"]
                for name in json_data:
                    style = Styler.load_json(json_data[name])
                    self.add(style, name)

    def get(self, name):
        return super().get(name)



styler_loader = StylerLoader()

if __name__ == "__main__":
    path = Path(r"C:\Users\Altron\PycharmProjects\MMO_project\src\data\configs\styles_config.json")
    styler_loader.load_styles(path)
