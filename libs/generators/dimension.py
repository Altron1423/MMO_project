from libs import loger, map_block_loader
from libs.generators import MapBlockGenerator
from libs.loaders.map_loader import MapLoader, map_loader
from libs.math import Position2
from libs.save.dimension import Dimension


class DimensionGeneratorTest:
    dimension: Dimension
    map_loader: MapLoader = map_loader

    def __init__(self, dimension: Dimension):
        self.dimension = dimension

    def gen1(self):
        loger.log("gen1")
        st_block = map_block_loader.get_new("start_test_block")
        MapBlockGenerator.gen1(st_block)
        self.dimension.add_map_block(
            st_block,
            Position2(2, 3)
        )
