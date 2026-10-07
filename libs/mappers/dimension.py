from dataclasses import dataclass

from libs.dtos import DimensionSaveDTO, DimensionConfigDTO
from libs.save.dimension import Dimension


@dataclass(frozen=True, slots=True)
class DimensionSaveMapper:

    @staticmethod
    def dto_to_dict(dto: DimensionSaveDTO) -> dict:
        return {
            "full_name": dto.full_name,
            "name": dto.name,
            "blocks": dto.blocks,
        }

    @staticmethod
    def dict_to_dto(data: dict) -> DimensionSaveDTO:
        return DimensionSaveDTO(
            full_name=data["full_name"],
            name=data["name"],
            blocks=data["blocks"]
        )

    @staticmethod
    def dim_to_dto(dim: Dimension) -> DimensionSaveDTO:
        return DimensionSaveDTO(
            full_name=str(dim),
            name=dim.name,
            blocks=[str(block) for block in dim.blocks]
        )

    @staticmethod
    def update_from_dto(dim: Dimension, dto: DimensionSaveDTO):
        dim.full_name = dto.full_name
        dim.name = dto.name

@dataclass(frozen=True, slots=True)
class DimensionConfigMapper:

    @staticmethod
    def dict_to_dto(data: dict) -> DimensionConfigDTO:
        return DimensionConfigDTO(
            name=data["name"],
            size=data["size"],
            blocks=data["blocks"]
        )
