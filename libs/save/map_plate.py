from libs.math import Position2


class MapPlate:
    id = 1

    name: str
    type: str
    position: Position2
    color: list[int]
    texture: None | str
    layer: int
    changeable: bool

    def __init__(self, name_plate: str):
        self.position = Position2()
        self.name = name_plate
        self.id = 0
        self.entities = []
        self.changeable = False

    def get_custom_data(self):
        return {}

    @property
    def Name(self):
        return self.name

    def __str__(self) -> str:
        return f"<{self.name}({self.id})>"

    def __copy__(self) -> "MapPlate":
        map_plate = MapPlate(self.name)
        map_plate.position = self.position + 0
        map_plate.id = MapPlate.id
        MapPlate.id += 1
        map_plate.type = self.type
        map_plate.changeable = self.changeable
        map_plate.color = self.color.copy()
        map_plate.texture = self.texture
        map_plate.layer = self.layer

        return map_plate
