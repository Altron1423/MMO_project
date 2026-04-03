from dataclasses import dataclass
from libs import Version
from libs.dtos.player import ClientPlayerDTO
from libs.math import Position2, Vector2


@dataclass
class AddressConnectDTO:
    ip: str
    port: int | None = None
    mac: str | None = None

@dataclass
class ConnectServerDTO:
    version: Version
    name: str
    address: AddressConnectDTO | None = None

@dataclass
class ConnectClientDTO:
    version: Version
    name: str
    password: str


@dataclass
class GameDataToServerDTO:
    move: Vector2
    speed: float
    target_position: Position2
    action: str | None = None

@dataclass
class GameDataToClientDTO:
    map_block: str
    player: ClientPlayerDTO
    chunk_position: Position2
    position: Position2
