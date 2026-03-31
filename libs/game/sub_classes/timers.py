from time import time

from dataclasses import dataclass
from typing import Callable, Any


@dataclass
class TimerDTO:
    """
    name:               название таймера
    activation_time:    время активации
    function:           запускаемая функция
    data_for_function:  дополнительная информация, передаваемая в функцию при запуске
    """
    name: str
    activation_time: int
    function: Callable
    data_for_function: Any


class Timers:
    timers: list[TimerDTO]
    rate: int
    next_update: float

    def __init__(self, rate=1):
        self.timers = []
        self.rate = rate
        self.next_update = time()

    def add(self, timer: TimerDTO | dict):
        if type(timer) == dict:
            timer = TimerDTO(
                timer["name"],
                time() + timer["activation_time"],
                timer["function"],
                timer["data_for_function"]
            )
        self.timers.append(timer)

    def update(self):
        if self.next_update <= time():
            self.next_update += self.rate
            timers = []
            for iT in self.timers:
                if iT.activation_time <= time():
                    iT.function(iT.data_for_function)
                else:
                    timers.append(iT)
            self.timers = timers
