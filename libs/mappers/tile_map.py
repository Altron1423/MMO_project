from dataclasses import dataclass

from ..math import Size2, Position2
from libs.dtos import (
    TileMapDTO
)


@dataclass(frozen=True, slots=True)
class TileMapMapper:

    @staticmethod
    def dto_to_dict(dto: TileMapDTO) -> dict[str, str]:
        return {
            "name": dto.name,
            "texture": dto.texture,
            "size": str(dto.size),
            "tiles": []
        }

    @staticmethod
    def dict_to_dto(data: dict) -> TileMapDTO:
        tiles = {}
        for i in data["tiles"]:
            i2 = tuple(tuple(map(int, g.split(","))) for g in i.split("/"))
            tiles[i2] = Position2(data["tiles"][i])
        return TileMapDTO(
            name=data["name"],
            texture=data["texture"],
            size=Size2(data["size"]),
            tiles=tiles
        )
