from dataclasses import dataclass

from libs.dtos import AttributeLayerEntityDTO, EntityToClientDTO
from libs.math import Position2, Vector2


@dataclass(frozen=True, slots=True)
class EntityToClientMapper:

    @staticmethod
    def dto_to_dict(dto: EntityToClientDTO) -> dict[str, str]:
        return {
            "name": dto.name,
            "position": str(dto.position),
            "health": str(dto.health),
            "orientation": str(dto.orientation),
            "visual_action": dto.visual_action
        }

    @staticmethod
    def dict_to_dto(data: dict) -> EntityToClientDTO:
        from libs import ProgressBar
        return EntityToClientDTO(
            name=data["name"],
            position=Position2(data["position"]),
            health=ProgressBar.init_from_str(data["health"]),
            orientation=Vector2(data["orientation"]),
            visual_action=data["visual_action"]
        )


@dataclass(frozen=True, slots=True)
class AttributeLayerEntityMapper:

    @staticmethod
    def dto_to_list(dto: AttributeLayerEntityDTO) -> list[int | float]:
        return [
            dto.constitution, dto.agility,
            dto.defense, dto.strength,
            dto.intellect, dto.spirit,
            dto.health_reg, dto.max_mana
        ]

    @staticmethod
    def list_to_dto(data: list) -> AttributeLayerEntityDTO:
        return AttributeLayerEntityDTO(
            constitution=data[0],
            agility=data[1],
            defense=data[2],
            strength=data[3],
            intellect=data[4],
            spirit=data[5],
            health_reg=data[6],
            max_mana=data[7]
        )


