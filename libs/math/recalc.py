from libs.math import Size2, Position2, Vector2

class Recalc:
    k: Vector2
    b: Vector2
    _type_: str = "Recalc"

    def __init__(self, k: Vector2 = None, b: Vector2 = None):
        if k is None:
            k = Vector2()
        if b is None:
            b = Position2()
        self.k = k
        self.b = b

    @classmethod
    def load_from_str(cls, raw_data: str) -> "Recalc":
        if raw_data[0] == '<' and raw_data[-1] == '>':
            data = raw_data[1:-1]
            tp, data = data.split(':', maxsplit=1)
            if tp != cls._type_:
                raise TypeError(f"{raw_data} string not {cls._type_}")
            return cls(*[Vector2(vec) for vec in data.split('/')])
        else:
            raise TypeError(f"{raw_data} only accepts strings for {cls._type_}")


    def value(self, size: Size2 | Position2):
        # print(size, self.k, self.b)
        return size * self.k + self.b

    def __add__(self, other):
        if isinstance(other, (Position2, Size2)):
            self.b += other
        elif isinstance(other, Vector2):
            self.k += other

    def __str__(self) -> str:
        return f"<{self._type_}:{self.k}/{self.b}>"

    @staticmethod
    def default() -> "Recalc":
        return Recalc(Vector2(), Vector2(10, 10))

    @staticmethod
    def default_very_faraway() -> "Recalc":
        return Recalc(Vector2(10, 10), Vector2(-1000, -1000))
