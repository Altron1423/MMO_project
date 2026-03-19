from libs.save.SaveLight import SaveLight


class SaveFull(SaveLight):

    def __init__(self, save_light: SaveLight):
        super().__init__(save_light.path_save)
        self.fast_load()

        self.full_load()

    def full_load(self):
        ...
