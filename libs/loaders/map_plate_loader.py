import json
from pathlib import Path

from libs import MapPlateConfigMapper
from libs.save.map_plate import MapPlate
from libs.loaders.loader import Loader


class MapPlateLoader(Loader):
    elements: dict[str, MapPlate]

    def __init__(self):
        self.elements = {}

    def load(self, path: Path) -> None:
        with Path(path).open("r", encoding="utf-8") as file:
            json_data = json.load(file)
            if json_data["type"] == "map_plate":

                data = MapPlateConfigMapper.dict_to_dto(json_data["data"])
                map_plate = MapPlate(data.name)
                map_plate.type = data.type
                map_plate.color = data.color
                map_plate.texture = data.texture
                map_plate.changeable = data.changeable

                self.add(map_plate, data.name)

    def load_from_dir(self, path: Path) -> None:
        for iPath in path.iterdir():
            self.load(iPath)

    def add(self, element: MapPlate, name: str) -> None:
        self.elements[name] = element

    def get(self, name: str) -> MapPlate | None:
        element = self.elements.get(name)
        return element

    def get_changeable(self, name: str) -> MapPlate | None:
        element = self.elements.get(name)
        if element.changeable:
            element = element.__copy__()
        return element

    def get_new(self, name: str) -> MapPlate | None:
        element = self.elements.get(name).__copy__()
        return element


map_plate_loader = MapPlateLoader()
