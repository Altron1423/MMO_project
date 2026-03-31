from dataclasses import dataclass
from typing import Callable, Any


@dataclass
class TriggersDTO:
    _min_limit:  Callable[[Any], Any] | None = None
    _below_zero: Callable[[Any], Any] | None = None
    _above_zero: Callable[[Any], Any] | None = None
    _limit:      Callable[[Any], Any] | None = None
    _increasing: Callable[[Any], Any] | None = None
    _decreasing: Callable[[Any], Any] | None = None

    def min_limit(self):
        if self._min_limit:
            self.min_limit()

    def below_zero(self):
        if self._below_zero:
            self.below_zero()

    def above_zero(self):
        if self._above_zero:
            self.above_zero()

    def limit(self):
        if self._limit:
            self.limit()

    def increasing(self):
        if self._increasing:
            self.increasing()

    def decreasing(self):
        if self._decreasing:
            self.decreasing()


class Bar:
    trigger_check = True
    value: int
    limit: int
    min_limit: int
    unlimit: bool
    triggers: TriggersDTO
    below_zero: bool

    def __init__(self, value:int=1, limit:int=100, min_value:int=0, unlimit:bool=False, triggers:TriggersDTO = TriggersDTO()):
        if type(value) in [list, tuple]:
            self.value, self.limit = value
        else:
            self.value = value
            self.limit = limit
        self.min_limit = min_value
        self.unlimit = unlimit
        self.triggers = triggers
        self.below_zero = False

    def trigger_activ(self, increase:bool):
        if self.trigger_check:
            if increase:
                if self.value >= self.limit:
                    if not self.unlimit:
                        self.value = self.limit
                    self.triggers.limit()
                if self.value >= 0 and self.below_zero:
                    self.below_zero = False
                    self.triggers.above_zero()
                self.triggers.increasing()
            else:
                if self.value <= self.min_limit:
                    if not self.unlimit:
                        self.value = self.min_limit
                    self.triggers.min_limit()
                if self.value <= 0 and self.below_zero == False:
                    self.below_zero = True
                    self.triggers.below_zero()
                self.triggers.decreasing()


    def update(self, value=0, limit=100):
        before = self.value
        if type(value) in [list, tuple]:
            self.value, self.limit = value
        else:
            self.value = value
            self.limit = limit
        self.trigger_activ((self.value - before) > 0)

    def get_full(self, from_zero=False):
        if from_zero:
            return self.value, self.limit
        else:
            return self.value - self.min_limit, self.limit - self.min_limit

    def __add__(self, dat: int):
        dat = int(dat)
        self.value += dat
        self.trigger_activ(dat > 0)

    def set_value(self, dat: int):
        old_value = self.value
        self.value = int(dat)
        self.trigger_activ((self.value - old_value) > 0)

    def add_limit(self, dat: int):
        self.limit += int(dat)
        self.trigger_activ(True)

    def set_limit(self, dat: int):
        self.limit = int(dat)
        self.trigger_activ(True)

    def add_min_limit(self, dat: int):
        self.min_limit += int(dat)
        self.trigger_activ(False)

    def set_min_limit(self, dat: int):
        self.min_limit = int(dat)
        self.trigger_activ(False)

    def __str__(self):
        return f"{self.value}/{self.limit}"
