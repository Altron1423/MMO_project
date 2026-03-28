from dataclasses import dataclass


@dataclass
class DimensionSaveDTO:
    full_name: str
    name: str
    blocks: list[str]

@dataclass
class DimensionConfigDTO:
    name: str
    size: str
    blocks: list[str]
