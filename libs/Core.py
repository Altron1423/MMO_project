from pathlib import Path
import json

from libs import Version

paths = ['saves_directory', 'logs_directory', 'mod_packs_directory']

class Core:
    version: Version
    saves_directory: Path
    logs_directory: Path
    mod_packs_directory: Path

    def __init__(self):
        path = Path.cwd()
        self.path = path.joinpath("src/data/configs/core.json")
        with self.path.open("r") as f:
            core = json.load(f)
        for i in core:
            if i in paths:
                self.__dict__[i] = path.joinpath(core[i])
            elif i == "version":
                self.__dict__[i] = Version(core[i])
            else:
                self.__dict__[i] = core[i]

CORE = Core()