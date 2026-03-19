from pathlib import Path
from datetime import datetime

from src.modules.dtos.save import (
    CreateSavesDTO,
    PresentationSaveDTO,
    CreateSaveWF_DTO
)
from libs.file_works.saves import SavesWF
from libs.Loger import loger
from libs.save.SaveFull import SaveFull
from libs.save.SaveLight import SaveLight

class SavesManager:
    path_saves: Path
    load_save: SaveFull | None
    saves: list[SaveLight] = []
    full_load_save: SaveFull | None
    using_dir: list[Path] = []

    @classmethod
    def set_path_save(cls, path_saves: Path) -> None:
        cls.path_saves = path_saves

    @classmethod
    def load_from_dir(cls) -> None:
        if cls.path_saves in cls.using_dir:
            return
        cls.using_dir.append(cls.path_saves)
        for iPath in cls.path_saves.iterdir():
            cls.__load_light_save(iPath)

    @classmethod
    def get_saves_name(cls) -> list[SaveLight]:
        saves_names = []
        for save in cls.saves:
            saves_names.append(save.name)
        return saves_names

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
        return cls.__load_full_save(save_name)

    @classmethod
    def __get_saves(cls, name: str) -> SaveLight | None:
        for i_save in cls.saves:
            if i_save.name == name:
                return i_save
        return None

    @classmethod
    def __load_light_save(cls, path: Path) -> None:
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
    def __load_full_save(cls, save_name: str) -> SaveFull | None:
        save = cls.__get_saves(save_name)
        if not save:
            return None
        full_save = SaveFull(save)
        return full_save



if __name__ == "__main__":
    saves = SavesManager()
    saves.set_path_save(Path.cwd().joinpath(r"/saves"))
    saves.load_from_dir()
    print(saves.get_saves_name())
    print(saves.get_preview_save('test_world'))

    saves.create_saves(CreateSavesDTO(
        name="test_world3",
        version=[0,1,0],
    ))
