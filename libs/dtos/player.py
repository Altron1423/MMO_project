from dataclasses import dataclass
from libs.math import Position2


@dataclass
class PlayerLoadDTO:
    race: str
    attributes: dict[str, list[int | float]]
    to_first_lvlup: int
    raising_xp: float
    xp_boost: float


@dataclass
class ClientPlayerDTO:
    name: str
    attributes: dict[str, list[int | float]] | None
    position: Position2
    health: "ProgressBar"
    mana: "ProgressBar"
    xp: "ProgressBar"
    lvl: int
    inventory: str
    map_block: str
