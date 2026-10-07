from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass
class CreateSavesDTO:
    name: str
    version: list[int]

@dataclass
class PresentationSaveDTO:
    name: str
    version: list[int]
    last_open: datetime
    description: str

@dataclass
class DataSaveDTO:
    name: str
    version: list[int]
    description: str
    last_open: datetime
    created: bool

@dataclass
class CreateSaveWF_DTO:
    name: str
    version: list[int]
    last_open: datetime
    description: str
    path_to_save: Path
    created: bool
