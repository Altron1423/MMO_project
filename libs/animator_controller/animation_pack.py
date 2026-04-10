import pygame as pg

from random import randint

from libs.math import Size2


class AnimationPack:
    size: Size2
    surfaces: list[pg.Surface]
    count: int
    time_to_surface: int
    _animation_seed: int


    def __init__(self):
        self.size = Size2()
        self.surfaces = []
        self.count = 0
        self._animation_seed = 0
        self.time_to_surface = 10

    def get_surface(self, tick: int = 0) -> pg.Surface:
        return self.surfaces[(tick + self._animation_seed) // self.time_to_surface % self.count]

    def add_surface(self, surface: pg.Surface):
        self.surfaces.append(surface)
        self.count += 1
        self._animation_seed = randint(0, self.count)

    def set_size(self, size: Size2):
        self.size = size
        self.__rescale_surface__()

    def set_time_to_surface(self, time_to_surface: int):
        self.time_to_surface = time_to_surface

    def set_scale(self, scale: float) -> "AnimationPack":
        self.size *= scale
        self.__rescale_surface__()
        return self

    def __rescale_surface__(self):
        for surf in range(self.count):
            self.surfaces[surf] = pg.transform.scale(self.surfaces[surf], self.size.tuple)

    def copy(self):
        return self.__copy__()

    def __copy__(self):
        animator_pack = AnimationPack()
        animator_pack.size = self.size
        animator_pack.surfaces = self.surfaces.copy()
        animator_pack.count = self.count
        animator_pack.time_to_surface = self.time_to_surface
        animator_pack._animation_seed = randint(0, self.count)
        return animator_pack
