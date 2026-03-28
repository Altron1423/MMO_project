from libs.save.map_chunk import MapChunk
from libs.math import Size2, Position2


class MapBlock:
    id: int = 1

    size: Size2
    position: Position2
    name: str
    form: list[
        list[
            MapChunk | None
        ]
    ]

    def __init__(self, size: Size2, name: str):
        self.size = size
        self.name = name
        self.position = Position2()
        self.id = 0
        self.form = []
        for z in range(size.z):
            self.form.append([None] * size.x)

    def set_form(self, form: list[list[MapChunk | None]]):
        for z in range(self.size.z):
            for x in range(self.size.x):
                self.form[z][x] = form[z][x]

    def set_chunk_on(
            self,
            chunk: MapChunk | None,
            position: Position2
    ) -> None:
        if position in self.size:
            self.form[position.z][position.x] = chunk

    @property
    def Name(self):
        return self.name

    def get_chunk(
            self,
            position: Position2,
    ) -> MapChunk:
        if position in self.size:
            return self.form[position.z][position.x]

    def __str__(self) -> str:
        return f"<{self.name}({self.id})>"

    def __copy__(self) -> "MapBlock":
        map_block = MapBlock(self.size, self.name)
        map_block.id = MapBlock.id
        MapBlock.id += 1
        map_block.__set_clone_form__(self.form)
        return map_block

    def __set_clone_form__(self, form: list[list[MapChunk | None]]) -> None:
        for x, z in self.size:
            if form[z][x] is not None:
                self.form[z][x] = form[z][x].__copy__()

