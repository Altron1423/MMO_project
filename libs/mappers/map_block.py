from dataclasses import dataclass

from libs import MapBlockSaveDTO, MapBlock, MapBlockConfigDTO
from libs.math import Position2


@dataclass(frozen=True, slots=True)
class MapBlockSaveMapper:

    @staticmethod
    def dto_to_dict(dto: MapBlockSaveDTO) -> dict:
        return {
            "full_name": dto.full_name,
            "name": dto.name,
            "id": dto.id,
            "position": dto.position,
            "chunks": dto.chunks
        }

    @staticmethod
    def dict_to_dto(data: dict) -> MapBlockSaveDTO:
        return MapBlockSaveDTO(
            full_name=data["full_name"],
            name=data["name"],
            id=data["id"],
            position=data["position"],
            chunks=data["chunks"]
        )

    @staticmethod
    def block_to_dto(map_block: MapBlock) -> MapBlockSaveDTO:
        return MapBlockSaveDTO(
            full_name=str(map_block),
            name=map_block.name,
            id=map_block.id,
            position=str(map_block.position),
            chunks=[
                [
                    str(chunk) if chunk else None
                    for chunk in line
                ]
                for line in map_block.form
            ]
        )

    @staticmethod
    def update_from_dto(block: MapBlock, dto: MapBlockSaveDTO):
        block.full_name = dto.full_name
        block.name = dto.name
        block.id = dto.id
        block.position = Position2(dto.position)

@dataclass(frozen=True, slots=True)
class MapBlockConfigMapper:

    @staticmethod
    def dict_to_dto(data: dict) -> MapBlockConfigDTO:
        return MapBlockConfigDTO(
            name=data["name"],
            size=data["size"],
            form=data["form"],
        )
