from dataclasses import dataclass


@dataclass
class MapPlateSaveDTO:
    full_name: str
    name: str
    id: int
    type: str
    custom_data: dict[str, str]

@dataclass
class MapPlateConfigDTO:
    name: str
    type: str
    color: list[int]
    texture: str
    changeable: bool
