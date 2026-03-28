import json
from pathlib import Path

from libs import loger, DimensionConfigMapper
from libs.save.dimension import Dimension
from libs.loaders import Loader
from libs.loaders import map_block_loader
from libs.math import Size2


class DimensionLoader(Loader):
    elements: dict[str, Dimension]

    def __init__(self):
        self.elements = {}

    def load(self, path: Path) -> None:
        with Path(path).open("r", encoding="utf-8") as file:
            json_data = json.load(file)
            if json_data["type"] == "dimension":
                data = DimensionConfigMapper.dict_to_dto(json_data["data"])
                size = Size2(data.size)
                dimension = Dimension(size, data.name)

                for block_name in data.blocks:
                    if map_block_loader.get(block_name):
                        dimension.add_using_block(block_name)

                self.add(dimension, data.name)

    def load_from_dir(self, path: Path) -> None:
        for iPath in path.iterdir():
            loger.log(f"Loading {iPath}")
            self.load(iPath)

    def add(self, element: Dimension, name: str) -> None:
        self.elements[name] = element

    def get(self, name: str) -> Dimension | None:
        element = self.elements.get(name)
        return element

    def get_new(self, name: str) -> Dimension | None:
        element = self.elements.get(name)
        return element.__copy__() if element else None


dimension_loader = DimensionLoader()
