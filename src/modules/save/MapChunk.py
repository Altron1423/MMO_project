from src.modules.math import Vector3
from MapPlate import MapPlate

class MapChunk:
    CountPlate:int = 16
    map: list[list[MapPlate]]

    def __init__(self):
        self.position = Vector3()
        self.map = [
            [MapPlate(self) for _ in range(self.CountPlate)] for _ in range(self.CountPlate)
        ]



