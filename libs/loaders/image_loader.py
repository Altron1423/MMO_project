from pathlib import Path
import pygame as pg
import json

from libs.loaders.loader import Loader


class ImageLoader(Loader):
    elements: dict[str, tuple[pg.Surface | None, str]]

    def load(self, path: Path):
        with path.open("r", encoding="utf-8") as file:
            json_data = json.load(file)
            if json_data["type"] == "image":
                json_data = json_data["images"]
                for name in json_data:
                    image = [None, json_data[name]]
                    self.add(image, name)

    def get(self, name: str) -> pg.Surface | None:
        image = self.elements.get(name)
        if image is None:
            return None
        elif image[0] is None:
            image[0] = pg.image.load(Path.cwd().joinpath(image[1]))
        return image[0]


image_loader = ImageLoader()
