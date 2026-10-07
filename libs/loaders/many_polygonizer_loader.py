from libs.graphics import ManyPolygonizer
from pathlib import Path
from libs.Loger import loger
import json

from libs.loaders.loader import Loader

if __name__ == '__main__':
    import pygame as pg
    pg.init()

class ManyPolygonizerLoader(Loader):
    elements: dict[str, ManyPolygonizer]

    def load(self, path: Path):
        with path.open("r", encoding="utf-8") as file:
            json_data = json.load(file)
            if json_data["type"] == "ManyPolygonizer":
                json_data = json_data["many_polygonizers"]
                for name in json_data:
                    many_polygon = ManyPolygonizer.load_json(json_data[name])
                    self.add(many_polygon, name)
            else:
                loger.log(f"Uncorrected Type {json_data["type"]}. Need type: \"ManyPolygonizer\"")

    def get(self, name:str) -> ManyPolygonizer | None:
        return super().get(name)



many_polygonizer_loader = ManyPolygonizerLoader()
if __name__ == "__main__":
    path = Path(r"C:\Users\Altron\PycharmProjects\MMO_project\src\data\configs\many_polygon_config.json")
    many_polygonizer_loader.load_manyPolygonizers(path)
