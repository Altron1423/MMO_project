from pathlib import Path

from . import Loader
from .map_plate_loader import MapPlateLoader, map_plate_loader
from .map_chunk_loader import MapChunkLoader,  map_chunk_loader
from .map_block_loader import MapBlockLoader, map_block_loader
from .dimension_loader import DimensionLoader, dimension_loader


class MapLoader(Loader):
    map_plate_loader: MapPlateLoader = map_plate_loader
    map_chunk_loader: MapChunkLoader = map_chunk_loader
    map_block_loader: MapBlockLoader = map_block_loader
    dimension_loader: DimensionLoader = dimension_loader

    def __init__(self):
        ...

    @classmethod
    def load_from_dir(cls, path_map: Path) -> None:
        map_plate_loader.load_from_dir(path_map.joinpath("plate"))
        map_chunk_loader.load_from_dir(path_map.joinpath("chunk"))
        map_block_loader.load_from_dir(path_map.joinpath("block"))
        dimension_loader.load_from_dir(path_map.joinpath("dimension"))

    # def load(self, path: Path) -> None:
    #     with Path(path).open("r", encoding="utf-8") as file:
    #         json_data = json.load(file)
    #         if json_data["type"] == "map_block":
    #             json_data = json_data["data"]
    #             size = Size2(json_data["size"])
    #             map_block = MapBlock(size)
    #             form = json_data["form"]
    #             for position in size:
    #                 if form[position.z][position.x] is not None:
    #                     map_block.set_chunk_on(
    #                         map_chunk_loader.get(
    #                             form[position.z][position.x],
    #                         ),
    #                         position
    #                     )
    #             self.add(map_block, json_data["name"])
    #
    # def add(self, element: MapBlock, name: str) -> None:
    #     self.elements[name] = element
    #
    # def get(self, name: str) -> MapBlock | None:
    #     element = self.elements.get(name)
    #     return element


map_loader = MapLoader()
