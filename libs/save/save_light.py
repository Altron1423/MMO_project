import json
from libs.dtos.save import (
    DataSaveDTO
)
# from libs.file_works.saves import SavesWF
from pathlib import Path
from datetime import datetime


class SaveLight:
    path_save: Path

    name: str
    version: list[int]
    last_open: datetime
    description: str
    created: bool

    def __init__(self, path):
        self.path_save = path

    def fast_load(self):
        from libs.file_works.saves import SavesWF

        SavesWF.load_save_light(self)


    def delete(self):
        from libs.file_works.saves import SavesWF
        SavesWF.delete(self.path_save)

