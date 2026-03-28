import json
from pathlib import Path

from libs import MapChunkConfigMapper
from libs.save.map_chunk import MapChunk
from libs.loaders.loader import Loader
from libs.loaders.map_plate_loader import map_plate_loader
from libs.math import Size2


class MapChunkLoader(Loader):
    elements: dict[str, MapChunk]

    def __init__(self):
        self.elements = {}

    def load(self, path: Path) -> None:
        with Path(path).open("r", encoding="utf-8") as file:
            json_data = json.load(file)
            if json_data["type"] == "map_chunk":
                data = MapChunkConfigMapper.dict_to_dto(json_data["data"])
                size = Size2(data.size)
                map_chunk = MapChunk(data.name, size)
                map_chunk.height_map = data.height_map
                plates = data.map_plates


                get_plate = lambda position: data.plates[str(plates[position.z][position.x])]
                for position in size:
                    map_chunk.set_plate_on(
                        map_plate_loader.get_changeable(
                            get_plate(position),
                        ),
                        position
                    )

                self.add(map_chunk, data.name)

    def load_from_dir(self, path: Path) -> None:
        for iPath in path.iterdir():
            self.load(iPath)

    def add(self, element: MapChunk, name: str) -> None:
        self.elements[name] = element

    def get(self, name: str) -> MapChunk | None:
        element = self.elements.get(name)
        return element

    def get_new(self, name: str) -> MapChunk | None:
        element = self.elements.get(name).__copy__()
        return element


map_chunk_loader = MapChunkLoader()
