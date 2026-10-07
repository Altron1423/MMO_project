from dataclasses import dataclass


@dataclass
class MapChunkSaveDTO:
    full_name: str
    name: str
    id: int
    changes_plates: dict[str, str]

@dataclass
class MapChunkConfigDTO:
    name: str
    size: str
    plates: dict[str, str]
    map_plates: list[list[str | int]]
    height_map: list[list[int]]
