from libs.math import Vector2
from libs.math import Size2

class Position2(Vector2):

    _vector_type_ = "Position"
    def __add__(self, other: int | Vector2 | Size2):
        pos = Position2()
        if isinstance(other, int):
            pos.set(self.x + other, self.z + other)
        elif isinstance(other, Position2):
            pos.set(self.x + other.x, self.z + other.z)
        elif isinstance(other, Size2):
            pos = self.__size_gen__(other)
        elif isinstance(other, Vector2):
            pos.set(self.x + other.x, self.z + other.z)
        return pos

    def __size_gen__(self, size: Size2):
        for position in size:
            yield self + position

    def __iter__(self):
        yield self.x
        yield self.z
