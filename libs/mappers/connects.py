from dataclasses import dataclass

from libs import Version
from libs.dtos import (
    ConnectServerDTO, ConnectClientDTO,
    GameDataToServerDTO, GameDataToClientDTO
)
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
            "chunk_position": str(dto.chunk_position),
            "position": str(dto.position),
        }

    @staticmethod
    def dict_to_dto(data: dict) -> GameDataToClientDTO:
        return GameDataToClientDTO(
            map_block=data["map_block"],
            chunk_position=Position2(data["chunk_position"]),
            position=Position2(data["position"]),
        )
