from libs import dimension_loader, SaveFull
from libs.generators import DimensionGeneratorTest


class SaveCreateTest:

    @staticmethod
    def create(save: SaveFull):
        dim = dimension_loader.get_new("start_test_dim")
        save.dimensions.append(dim)
        dim_gen = DimensionGeneratorTest(dim)
        data = dim_gen.gen1()
        if data is not None:
            save.spawn_position, save.spawn_map_block = data
        save.created = True
