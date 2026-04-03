from libs.math import Position2, Size2
from .map_plate import MapPlate

class MapChunk:
    id: int = 1

    name: str
    position: Position2
    size: Size2
    map: list[
        list[
            MapPlate | None
        ]
    ]
    height_map: list[
        list[
            int
        ]
    ]

    def __init__(self, name: str, size: Size2):
        self.position = Position2()
        self.name = name
        self.size = size
        self.id = 0
        self.map = [
            [None] * self.size.x for _ in range(self.size.z)
        ]
        # self.height_map = [
        #     [None] * self.size.x for _ in range(self.size.z)
        # ]


    def set_plate_on(
            self,
            plate: MapPlate,
            position: Position2
    ) -> None:
        if position in self.size:
            self.map[position.z][position.x] = plate

    @property
    def Name(self):
        return self.name

    def get_plate(
            self,
            position: Position2,
    ) -> MapPlate:
        if position in self.size:
            return self.map[position.z][position.x]
        raise f"{position} not in {self.size}"

    def get_height(
            self,
            position: Position2,
    ) -> int:
        if position in self.size:
            return self.height_map[position.z][position.x]
        raise f"{position} not in {self.size}"

    def __str__(self) -> str:
        return f"<{self.name}({self.id})>"

    def __copy__(self) -> "MapChunk":
        map_chunk = MapChunk(self.name, self.size)
        map_chunk.position = self.position + 0
        map_chunk.id = MapChunk.id
        MapChunk.id += 1
        map_chunk.height_map = self.height_map
        map_chunk.__set_clone_map__(self.map)
        return map_chunk

    def __set_clone_map__(self, map: list[list[MapPlate | None]]) -> None:
        for x, z in self.size:
            map_plate = map[z][x]
            if map_plate.changeable:
                map_plate = map_plate.__copy__()

            self.map[z][x] = map_plate
