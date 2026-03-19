from pathlib import Path
import json

paths = ['saves_directory', 'logs_directory', 'mod_packs_directory']

class Core:
    version: list[int]
    saves_directory: str
    logs_directory: str
    mod_packs_directory: str

    def __init__(self):
        path = Path.cwd()
        self.path = path.joinpath("src/data/configs/core.json")
        with self.path.open("r") as f:
            core = json.load(f)
        for i in core:
            if i in paths:
                self.__dict__[i] = path.joinpath(core[i])
            elif i == "version":
                self.__dict__[i] = list(map(int, core[i].split(".")))

CORE = Core()