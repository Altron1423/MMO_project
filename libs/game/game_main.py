from pathlib import Path

from . import GameStartException
from libs.save import SaveFull
from libs.generators import SaveCreateTest
from ..Loger import loger
from ..loaders import map_loader


class GameMain:
    save: SaveFull

    def __init__(self):
        path_map = Path.cwd().joinpath("src/data/map")

        map_loader.load_from_dir(path_map)

        loger.status("GameMain loaded complete")

    def set_game_save(self, save_full: SaveFull):
        self.save = save_full
        if self.save.need_created():
            SaveCreateTest.create(self.save)

    def start(self):
        if not self.save:
            raise GameStartException()
        loger.status("GameMain started")

    def saving(self):
        self.save.saving()