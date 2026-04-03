from dataclasses import dataclass

from libs.dtos import AttributeLayerEntityDTO


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


