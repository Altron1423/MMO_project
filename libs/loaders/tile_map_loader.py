import json
from pathlib import Path
import pygame as pg

from . import Loader
from .image_loader import image_loader
# from .. import Size2
from ..mappers import TileMapMapper

def f(value: int, name: str) -> str | None:
    if value == 1:
        return name
    else:
        return None

T = tuple[str, str]
T2 = tuple[T, T]


class TileMapLoader(Loader):
    elements: dict[T2, pg.Surface]

    def load(self, path: Path) -> None:
        with path.open("r", encoding="utf-8") as file:
            json_data = json.load(file)
            if json_data["type"] == "tile_map":
                data = TileMapMapper.dict_to_dto(json_data["data"])
                size = data.size
                image = image_loader.get(data.texture)
                for tile in data.tiles:
                    tile_r = (
                        (f(tile[0][0], data.name), f(tile[0][1], data.name)),
                        (f(tile[1][0], data.name), f(tile[1][1], data.name))
                    )
                    pos = data.tiles[tile]
                    surf = pg.Surface(data.size.tuple, pg.SRCALPHA)
                    surf.blit(
                        image,
                        (
                            -size.x * pos.x,
                            -size.z * pos.z
                        )
                    )
                    self.add(surf, tile_r)

    def add(self, surf: pg.Surface, tile_r: T2) -> None:
        self.elements[tile_r] = surf

    def get(self, name: T2) -> pg.Surface | None:
        element = self.elements.get(name)
        return element



tile_map_loader = TileMapLoader()

