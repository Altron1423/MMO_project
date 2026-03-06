import json
from src.modules.dtos.save import (
    DataSaveDTO
)
from src.modules.file_works.saves import SavesWF
from pathlib import Path
from datetime import datetime


class SaveLight:
    path_save: Path

    name: str
    data: DataSaveDTO
    version: list[int]
    last_open: datetime
    description: str
    options: dict

    def __init__(self, path):
        self.path_save = path

    def fast_load(self):
        with open(f"{self.path_save}\\main.json", "r", encoding="utf-8") as f:
            self.data = json.load(f)

        self.data = SavesWF.get_save_info(self.path_save)

        for i_data in self.data.__dict__:
            self.__dict__[i_data] = self.data.__dict__[i_data]

        self.version = list(map(int, self.version.split(".")))
        self.options = {}

