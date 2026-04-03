from typing import Any, Callable

import pygame as pg

KeysTransf = {
    pg.K_q: "q", pg.K_w: "w", pg.K_e: "e", pg.K_r: "r", pg.K_t: "t", pg.K_y: "y",
    pg.K_u: "u", pg.K_i: "i", pg.K_o: "o", pg.K_p: "p", pg.K_a: "a", pg.K_s: "s",
    pg.K_d: "d", pg.K_f: "f", pg.K_g: "g", pg.K_h: "h", pg.K_j: "j", pg.K_k: "k",
    pg.K_l: "l", pg.K_z: "z", pg.K_x: "x", pg.K_c: "c", pg.K_v: "v", pg.K_b: "b",
    pg.K_n: "n", pg.K_m: "m", pg.K_0: "0", pg.K_1: "1", pg.K_2: "2", pg.K_3: "3",
    pg.K_4: "4", pg.K_5: "5", pg.K_6: "6", pg.K_7: "7", pg.K_8: "8", pg.K_9: "9",
    pg.K_SPACE: " ", pg.K_COMMA: ",", pg.K_PERIOD: ".", pg.K_SLASH: "/", pg.K_MINUS: "-"
}

class TriggerGen:
    triggers: dict[tuple[str, bool] | tuple[int, bool], Callable[["Button"], Any]]

    def __init__(self):
        self.triggers = {}
        self.last = None

    def LMD(self, function: Callable[["Button"], Any]):
        self.triggers[(1, True)] = function
        return self

    def LMU(self, function: Callable[["Button"], Any]):
        self.triggers[(1, False)] = function
        return self

    def RMD(self, function: Callable[["Button"], Any]):
        self.triggers[(3, True)] = function
        return self

    def RMU(self, function: Callable[["Button"], Any]):
        self.triggers[(3, False)] = function
        return self

    def MWD(self, function: Callable[["Button"], Any]):
        self.triggers[(4, False)] = function
        return self

    def MWU(self, function: Callable[["Button"], Any]):
        self.triggers[(5, False)] = function
        return self

    def HoldD(self, function: Callable[["Button"], Any]):
        self.triggers[('hold', True)] = function
        return self

    def HoldU(self, function: Callable[["Button"], Any]):
        self.triggers[('hold', False)] = function
        return self

    def key_down(self, key, function: Callable[["Button"], Any]):
        self.triggers[(key, True)] = function
        return self

    def key_up(self, key, function: Callable[["Button"], Any]):
        self.triggers[(key, False)] = function
        return self

    def __iadd__(self, other):
        if type(other) == dict:
            for k, f in other.items():
                self.triggers[k] = f
        elif isinstance(other, self.__class__):
            for k, f in other.triggers.items():
                self.triggers[k] = f
        return self

    def __getitem__(self, key) -> Callable[["Button"], Any] | None:
        if key in self.triggers:
            self.last = key
            return self.triggers[key]
        return None

