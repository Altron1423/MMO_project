from collections.abc import Callable


# class Event:
#     date: int
#     more: bool
#
#     def __init__(self, date: int, more: bool=False):
#         self.date = date
#         self.more = more
#
#     def test(self, date: int):
#         if self.more:
#             return date >= self.date
#         else:
#             return date == self.date
#
# class Tick:
#     _tick_: int
#     events: list[tuple[Event, Callable[[int], None]]]
#
#     def __init__(self):
#         self._tick_ = 0
#         self.events = []
#
#     def tick(self):
#         self._tick_ += 1
#         breaking = False
#         for event in self.events:
#             if event[0].test(self._tick_):
#                 self.events.remove(event)
#                 event[1](self._tick_)
#                 breaking = True
#             elif breaking:
#                 break
#
#     def add_event(self, date: int | Event, event: Callable[[int], any]):
#         if isinstance(date, int):
#             date = Event(date)
#         x = date.date
#         i = 0
#         ln = len(self.events)
#         events = []
#         while i < ln and x < self.events[i][0].date:
#             events.append(self.events[i])
#         events.append((date, event))
#         events += self.events[i:]
#         self.events = events
#
#     def __int__(self):
#         return self._tick_
#
#     def __str__(self):
#         return f"<Tick:{self._tick_}>"
#
#     def __mod__(self, other: int) -> bool:
#         return self._tick_ % other == 0

class Tick:
    _tick_: int
    events: list[tuple[int, Callable[[int], None]]]

    def __init__(self):
        self._tick_ = 0
        self.events = []

    def tick(self):
        self._tick_ += 1
        for i in range(len(self.events)):
            if self.events[i][0] == self._tick_:
                self.events[i][1](self._tick_)
            elif self.events[i][0] > self._tick_:
                self.events = self.events[i:]
                break


    def add_event(self, date: int, event: Callable[[int], any]):
        i = 0
        ln = len(self.events)
        events = []
        while i < ln and self.events[i][0] <= date:
            events.append(self.events[i])
            i += 1
        events.append((date, event))
        events += self.events[i:]
        self.events = events

    def __int__(self):
        return self._tick_

    def __str__(self):
        return f"<Tick:{self._tick_}>"

    def __mod__(self, other: int) -> bool:
        return self._tick_ % other == 0



class Ticker:
    _tick_: Tick
    custom_ticks: dict[str, Tick]

    def __init__(self):
        self._tick_ = Tick()
        self.custom_ticks = {}

    def tick(self):
        self._tick_.tick()
        for tick_name in self.custom_ticks:
            self.custom_ticks[tick_name].tick()

    def add_tick(self, tick_name: str):
        self.custom_ticks[tick_name] = Tick()

    def get(self, tick_name: str | None = None) -> Tick | None:
        if tick_name is None:
            return self._tick_
        elif tick_name in self.custom_ticks:
            return self.custom_ticks[tick_name]
        return None

    def __int__(self):
        return self._tick_

    def __str__(self):
        return str(self._tick_)

    def __mod__(self, other: int) -> bool:
        return self._tick_ % other




if __name__ == "__main__":
    ticker = Ticker()
    for _ in range(10):
        ticker.tick()
        print(ticker, ticker % 2, ticker % 3)
    # tick = Tick()
    #
    # tick.add_event(4, lambda x: print("hello"))
    # tick.add_event(4, lambda x: print("hello"))
    # tick.add_event(5, lambda x: print("hello"))
    # tick.add_event(6, lambda x: print("hello"))
    # for _ in range(10):
    #     tick.tick()
    #     print(tick, tick % 2, tick % 3)
