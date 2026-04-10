from dataclasses import dataclass

from libs import Version
from libs.mappers import ClientPlayerMapper
from libs.dtos import (
    ConnectServerDTO, ConnectClientDTO,
    GameDataToServerDTO, GameDataToClientDTO
)
from libs.mappers.entity import EntityToClientMapper
from libs.math import Position2, Vector2


@dataclass(frozen=True, slots=True)
class ConnectServerMapper:

    @staticmethod
    def dto_to_dict(dto: ConnectServerDTO) -> dict[str, str]:
        return {
            "version": str(dto.version),
            "name": dto.name,
        }

    @staticmethod
    def dict_to_dto(data: dict) -> ConnectServerDTO:
        return ConnectServerDTO(
            name=data["name"],
            version=Version(data["version"]),
        )

@dataclass(frozen=True, slots=True)
class ConnectClientMapper:

    @staticmethod
    def dto_to_dict(dto: ConnectClientDTO) -> dict[str, str]:
        return {
            "version": str(dto.version),
            "name": dto.name,
            "password": dto.password
        }

    @staticmethod
    def dict_to_dto(data: dict) -> ConnectClientDTO:
        return ConnectClientDTO(
            name=data["name"],
            version=Version(data["version"]),
            password=data["password"]
        )

@dataclass(frozen=True, slots=True)
class GameDataToServerMapper:

    @staticmethod
    def dto_to_dict(dto: GameDataToServerDTO) -> dict[str, str]:
        return {
            "move": str(dto.move),
            "speed": dto.speed,
            "target_position": str(dto.target_position),
            "action": dto.action
        }

    @staticmethod
    def dict_to_dto(data: dict[str, list[float] | float | str]) -> GameDataToServerDTO:
        return GameDataToServerDTO(
            move=Vector2(data["move"]),
            speed=data["speed"],
            target_position=Position2(data["target_position"]),
            action=data["action"]
        )

@dataclass(frozen=True, slots=True)
class GameDataToClientMapper:

    @staticmethod
    def dto_to_dict(dto: GameDataToClientDTO) -> dict[str, str]:
        return {
            "map_block": dto.map_block,
            "entities": [EntityToClientMapper.dto_to_dict(g) for g in dto.entities],
            "player": ClientPlayerMapper.dto_to_dict(dto.player),
            "chunk_position": str(dto.chunk_position),
            "position": str(dto.position),
        }

    @staticmethod
    def dict_to_dto(data: dict) -> GameDataToClientDTO:
        return GameDataToClientDTO(
            map_block=data["map_block"],
            entities=[EntityToClientMapper.dict_to_dto(g) for g in data["entities"]],
            player=ClientPlayerMapper.dict_to_dto(data["player"]),
            chunk_position=Position2(data["chunk_position"]),
            position=Position2(data["position"]),
        )
