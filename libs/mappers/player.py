from dataclasses import dataclass

from libs.dtos import (
    PlayerLoadDTO, ClientPlayerDTO
)
from libs.math import Position2




@dataclass(frozen=True, slots=True)
class PlayerLoadMapper:

    @staticmethod
    def dto_to_dict(dto: PlayerLoadDTO) -> dict[str, str | dict | int | float]:
        return {
            "race": dto.race,
            "attributes": dto.attributes,
            "to_first_lvlup": dto.to_first_lvlup,
            "raising_xp": dto.raising_xp,
            "xp_boost": dto.xp_boost,
        }

    @staticmethod
    def dict_to_dto(data: dict) -> PlayerLoadDTO:
        return PlayerLoadDTO(
            race=data["race"],
            attributes=data["attributes"],
            to_first_lvlup=data["to_first_lvlup"],
            raising_xp=data["raising_xp"],
            xp_boost=data["xp_boost"],
        )


@dataclass(frozen=True, slots=True)
class ClientPlayerMapper:

    @staticmethod
    def dto_to_dict(dto: ClientPlayerDTO) -> dict[str, str]:
        return {
            "name": dto.name,
            "attributes": dto.attributes,
            "position": str(dto.position),
            "health": str(dto.health),
            "mana": str(dto.mana),
            "xp": str(dto.xp),
            "lvl": dto.lvl,
            "inventory": str(dto.inventory),
        }

    @staticmethod
    def dict_to_dto(data: dict) -> ClientPlayerDTO:
        from libs import ProgressBar
        return ClientPlayerDTO(
            name=data["name"],
            attributes=data["attributes"],
            position=Position2(data["position"]),
            health=ProgressBar.init_from_str(data["health"]),
            mana=ProgressBar.init_from_str(data["mana"]),
            xp=ProgressBar.init_from_str(data["xp"]),
            lvl=data["lvl"],
            inventory=data["inventory"],
        )
