from . import BlockNotInDimensionException
from .map_block import MapBlock
from .map_chunk import MapChunk
from libs.math import Position2, Size2


class Dimension:
    id: int = 0

    size: Size2
    name: str
    map_matrix: list[list[MapChunk | None]]
    blocks: list[MapBlock]
    using_blocks: list[str]

    def __init__(self, size: Size2, name: str) -> None:
        self.size = size
        self.name = name
        self.map_matrix = []

        for _ in range(size.z):
            self.map_matrix.append([None] * size.x)

        self.blocks = []
        self.using_blocks = []

    def add_map_block(
            self,
            map_block: MapBlock,
            position: Position2 = None
    ) -> bool:
        if position is None:
            position = map_block.position
        else:
            map_block.position = position

        if map_block.name not in self.using_blocks:
            raise BlockNotInDimensionException(f"Блок <{map_block.name}>, не может существовать в <{self.name}>.")
        if not self.test_block_on_matrix(position, map_block):
            return False

        # map_block.generate_chunks()
        self.__set_block__(map_block, position)
        return True

    def add_using_block(self, map_block: str) -> None:
        self.using_blocks.append(map_block)

    def test_block_on_matrix(
            self,
            position: Position2,
            map_block: MapBlock
    ) -> bool:
        for x, z in position + map_block.size:
            if self.map_matrix[x][z] is not None:
                return False
        return True

    @property
    def Name(self):
        return self.name

    def get_chunk(self, position: Position2) -> MapChunk:
        if position in self.size:
            return self.map_matrix[position.z][position.x]

    def __set_block__(
            self,
            map_block: MapBlock,
            position: Position2 = None
    ) -> None:
        self.blocks.append(map_block)

        for xb, zb in map_block.size:
            d_pos = position + Position2(xb, zb)
            self.map_matrix[d_pos.z][d_pos.x] = map_block.form[zb][xb]

    def __str__(self) -> str:
        return f"<{self.name}({self.id})>"

    def __copy__(self) -> "Dimension":
        dim = Dimension(self.size, self.name)
        dim.id = Dimension.id
        Dimension.id += 1
        dim.blocks = self.blocks.copy()
        dim.using_blocks = self.using_blocks.copy()
        dim.__fill_matrix_map__()
        return dim

    def __fill_matrix_map__(self) -> None :
        for map_block in self.blocks:
            self.__set_block__(map_block)

