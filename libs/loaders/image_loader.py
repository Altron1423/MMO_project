from pathlib import Path
import pygame as pg
import json


class ImageLoader:

    def __init__(self):
        self.images = {}

    def load_images(self, path):
        with Path(path).open("r", encoding="utf-8") as file:
            json_data = json.load(file)
            if json_data["type"] == "image":
                json_data = json_data["images"]
                for name in json_data:
                    image = [None, json_data[name]]
                    self.add_image(image, name)

    def add_image(self, image, name):
        self.images[name] = image

    def get_image(self, name):
        image = self.images.get(name)
        if image is None:
            return None
        elif image[0] is None:
            image[0] = pg.image.load(Path.cwd().joinpath(image[1]))
        return image[0]


image_loader = ImageLoader()
