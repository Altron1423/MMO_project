import json
from src.modules.Loger import log, status
from pathlib import Path

class Save:
    data: dict
    version: list[int]
    options: dict

    def __init__(self, path):
        self.path = path

    def fast_load(self):
        with open(f"{self.path}\\main.json", "r", encoding="utf-8") as f:
            self.data = json.load(f)
        self.version = list(map(int, self.data["version"].split(".")))
        self.options = {}

    def full_load(self):
        ...


class SaveManager:
    saves: list[Save]
    def __init__(self):
        self.saves = []

    def load_from_dir(self, path:Path):

        for iPath in path.iterdir():
            self._load_save(iPath)

    def _load_save(self, path:Path):
        status("load save from:", path)
        save = Save(path)
        save.fast_load()
        self.saves.append(save)
        log(save.__dict__)


if __name__ == "__main__":
    saves = SaveManager()
    saves.load_from_dir(Path.cwd().joinpath(r"/src/saves"))

