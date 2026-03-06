import os
from pathlib import Path
import json

from src.modules.dtos.save import CreateSaveWF_DTO, DataSaveDTO


class SavesWF:
    @classmethod
    def get_save_info(cls, path_save_directory: Path) -> DataSaveDTO:
        with open(f"{path_save_directory}\\main.json", "r", encoding="utf-8") as f:
            dt = json.load(f)
            print(dt)
            data = DataSaveDTO(
                **dt
            )
        return data

    @classmethod
    def create_save(cls, create_save: CreateSaveWF_DTO) -> None:
        print(create_save)
        path = create_save.path_to_save.joinpath(create_save.name)
        os.mkdir(path)
        with open(path.joinpath("main.json"), "a", encoding="utf-8") as file:
            json.dump({
                "name": create_save.name,
                "version": ".".join(map(str, create_save.version)),
                "description": create_save.description,
                "last_open": str(create_save.last_open),
            }, file)