import json
from pathlib import Path

from libs import MapBlockConfigMapper
from libs.save.map_block import MapBlock
from libs.loaders import map_chunk_loader
from libs.loaders import Loader
from libs.math import Size2


class MapBlockLoader(Loader):
    elements: dict[str, MapBlock]

    def __init__(self):
        self.elements = {}

    def load(self, path: Path) -> None:
        with Path(path).open("r", encoding="utf-8") as file:
            json_data = json.load(file)
            if json_data["type"] == "map_block":
                data = MapBlockConfigMapper.dict_to_dto(json_data["data"])
                size = Size2(data.size)
                map_block = MapBlock(
                    size,
                    data.name
                )

                form = data.form
                for position in size:
                    if form[position.z][position.x] is not None:
                        map_block.set_chunk_on(
                            map_chunk_loader.get(
                                form[position.z][position.x],
                            ),
                            position
                        )
                self.add(map_block, data.name)

    def load_from_dir(self, path: Path) -> None:
        for iPath in path.iterdir():
            self.load(iPath)

    def add(self, element: MapBlock, name: str) -> None:
        self.elements[name] = element

    def get(self, name: str) -> MapBlock | None:
        element = self.elements.get(name)
        return element

    def get_new(self, name: str) -> MapBlock | None:
        return self.get(name).__copy__()


map_block_loader = MapBlockLoader()
