from libs.Loger import loger
from libs.math import Position2
from libs.save import (
    SaveLight, Dimension, MapBlock
)


class SaveFull(SaveLight):
    spawn_map_block: MapBlock
    spawn_position: Position2

    dimensions: list[Dimension]


    def __init__(self, save_light: SaveLight):
        super().__init__(save_light.path_save)

        from libs.file_works import SavesWF

        self.saves_wf = SavesWF
        self.fast_load()

        self.full_load()
        loger.status(f"SaveFull \"{self.name}\" loaded")

    def full_load(self):
        self.dimensions = []
        if self.created:
            sw = self.saves_wf(self.path_save)
            sw.load_save_full(self)
            self.__load__()

    def need_created(self) -> bool:
        return self.created is False

    def saving(self):
        s_wf = self.saves_wf(self.path_save)
        s_wf.saving(self)

    def __load__(self):
        ...
