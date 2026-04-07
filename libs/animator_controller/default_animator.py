import pygame as pg
from .animation_pack import AnimationPack
from libs.math import Size2
from libs.ticker import Tick

class DefaultAnimator:
    default_surface: dict[str, AnimationPack]
    default_size: Size2
    first_scale: float
    second_scale: float
    scale_surface: dict[str, AnimationPack]
    type: str | None
    tick: Tick

    def __init__(self, tick: Tick):
        self.default_surface = {}
        self.first_scale = 1.0
        self.second_scale = 1.0
        self.scale_surface = {}
        self.type = None
        self.tick = tick

    def get_surface(self) -> None | pg.Surface:
        if self.type is None:
            return None
        return self.scale_surface[self.type].get_surface(int(self.tick))

    def add_animation_pack(self, name: str, animator_pack: AnimationPack):
        self.default_surface[name] = animator_pack
        animator_pack = animator_pack.copy()
        animator_pack.set_scale(self.second_scale)
        self.scale_surface[name] = animator_pack

    def set_type(self, type_d: str):
        if type_d in self.default_surface:
            self.type = type_d

    def set_scale(self, scale: float):
        if self.second_scale != scale:
            self.second_scale = scale
            self.__rescale__()
        else:
            self.second_scale = scale

    def set_default_size(self, size: Size2):
        self.default_size = size

    def set_size(self, size: Size2):
        self.first_scale = (size / self.default_size).x

    def __rescale__(self):
        for name in self.default_surface:
            self.scale_surface[name] = self.default_surface[name].copy().set_scale(self.first_scale * self.second_scale)

