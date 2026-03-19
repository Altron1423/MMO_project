from __dop.src2.graphics.polygons import ManyPolygonizer
from pathlib import Path
from __dop.src2.data.Loger import log
import json

if __name__ == '__main__':
    import pygame as pg
    pg.init()

class ManyPolygonizerLoader:
    def __init__(self):
        self.many_polygonizers = {}

    def load_manyPolygonizers(self, path):
        with Path(path).open("r", encoding="utf-8") as file:
            json_data = json.load(file)
            if json_data["type"] == "ManyPolygonizer":
                json_data = json_data["many_polygonizers"]
                for name in json_data:
                    many_polygon = ManyPolygonizer.load_json(json_data[name])
                    self.add_polygonizer(many_polygon, name)
            else:
                log(f"Uncorrected Type {json_data["type"]}. Need type: \"ManyPolygonizer\"")

    def add_polygonizer(self, style, name):
        self.many_polygonizers[name] = style

    def get_polygonizer(self, name):
        return self.many_polygonizers[name]



many_polygonizer_loader = ManyPolygonizerLoader()
if __name__ == "__main__":
    path = Path(r"/src2\data\configs\many_polygon_config.json")
    many_polygonizer_loader.load_manyPolygonizers(path)
