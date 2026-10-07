from pathlib import Path

from . import Loader
from .map_plate_loader import MapPlateLoader,   map_plate_loader
from .map_chunk_loader import MapChunkLoader,   map_chunk_loader
from .map_block_loader import MapBlockLoader,   map_block_loader
from .dimension_loader import DimensionLoader,  dimension_loader
from .tile_map_loader  import TileMapLoader,    tile_map_loader


class MapLoader(Loader):
    map_plate_loader: MapPlateLoader  = map_plate_loader
    map_chunk_loader: MapChunkLoader  = map_chunk_loader
    map_block_loader: MapBlockLoader  = map_block_loader
    dimension_loader: DimensionLoader = dimension_loader
    tile_map_loader:  TileMapLoader   = tile_map_loader

    def __init__(self):
        ...

    @classmethod
    def load_from_dir(cls, path_map: Path) -> None:
        map_plate_loader.load_from_dir(path_map.joinpath("plate"))
        map_chunk_loader.load_from_dir(path_map.joinpath("chunk"))
        map_block_loader.load_from_dir(path_map.joinpath("block"))
        dimension_loader.load_from_dir(path_map.joinpath("dimension"))
        tile_map_loader.load_from_dir(path_map.joinpath("tile_map"))

map_loader = MapLoader()
