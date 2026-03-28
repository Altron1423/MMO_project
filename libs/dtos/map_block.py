from dataclasses import dataclass


@dataclass
class MapBlockSaveDTO:
    full_name: str
    name: str
    id: int
    position: str
    chunks: list[list[str | None]]

@dataclass
class MapBlockConfigDTO:
    name: str
    size: str
    form: list[list[str | None]]
