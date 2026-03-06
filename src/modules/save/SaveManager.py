from pathlib import Path
from datetime import datetime

from src.modules.dtos.save import (
    CreateSavesDTO,
    PresentationSaveDTO,
    CreateSaveWF_DTO
)
from src.modules.file_works.saves import SavesWF
from src.modules.Loger import loger
from src.modules.save.SaveFull import SaveFull
from src.modules.save.SaveLight import SaveLight

class SavesManager:
    path_saves: Path
    load_save: SaveFull | None
    saves: list[SaveLight] = []

    @classmethod
    def set_path_save(cls, path_saves: Path) -> None:
        cls.path_saves = path_saves

    @classmethod
    def load_from_dir(cls) -> None:
        for iPath in cls.path_saves.iterdir():
            cls._load_save(iPath)

    @classmethod
    def _load_save(cls, path: Path) -> None:
        try:
            loger.status("load save from:", path)
            save = SaveLight(path)
            save.fast_load()
            cls.saves.append(save)
            loger.log(save.__dict__)
        except Exception as e:
            loger.status("load save failed")
            loger.error(e)

    @classmethod
    def get_saves_name(cls) -> list[SaveLight]:
        saves_names = []
        for save in cls.saves:
            saves_names.append(save.name)
        return saves_names

    @classmethod
    def _get_saves(cls, name: str) -> SaveLight | None:
        for i_save in cls.saves:
            if i_save.name == name:
                return i_save
        return None

    @classmethod
    def get_preview_save(cls, name_save: str) -> PresentationSaveDTO | None:
        save_element = cls._get_saves(name_save)

        if not save_element:
            return None

        return PresentationSaveDTO(
            name=save_element.name,
            version=save_element.version,
            last_open=save_element.last_open,
            description=save_element.description,
        )

    @classmethod
    def create_saves(cls, save: CreateSavesDTO) -> bool:
        if save.name in cls.get_saves_name():
            return False

        SavesWF.create_save(CreateSaveWF_DTO(
            name=save.name,
            version=save.version,
            last_open=datetime.now(),
            description="",
            path_to_save=cls.path_saves
        ))

        return True

    @classmethod
    def load_full_save(cls, save_name: str) -> SaveFull:
        save = cls._get_saves(save_name)


if __name__ == "__main__":
    saves = SavesManager()
    saves.set_path_save(Path.cwd().joinpath(r"D:\JetBrains\project\PycharmProjects\MMO_project\saves"))
    saves.load_from_dir()
    print(saves.get_saves_name())
    print(saves.get_preview_save('test_world'))

    saves.create_saves(CreateSavesDTO(
        name="test_world3",
        version=[0,1,0],
    ))
