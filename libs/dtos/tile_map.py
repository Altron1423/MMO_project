from dataclasses import dataclass

from ..math import Size2, Position2

T = tuple[int, int]

@dataclass
class TileMapDTO:
    name: str
    texture: str
    size: Size2
    tiles: dict[
        tuple[T, T],
        Position2
    ]
