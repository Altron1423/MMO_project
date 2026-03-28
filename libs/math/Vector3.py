from .Vector2 import Vector2

class Vector3:
    x: int
    y: int
    z: int
    _vector_type_ = "Vector3"

    def __init__(self, *position):
        self.set(*position)

    def set(self, *position):
        position += [0] * (3 - len(position))
        self.x, self.y, self.z = position

    def __mul__(self, other):
        pos = Vector3()

        if isinstance(other, int):
            pos.set(self.x * other, self.y * other, self.z * other)
        elif isinstance(other, Vector3):
            pos.set(self.x * other.x, self.y, self.z * other.z)

        return pos

    def __add__(self, other):
        pos = Vector3()

        if isinstance(other, int):
            pos.set(self.x + other, self.y + other, self.z + other)
        elif isinstance(other, Vector3):
            pos.set(self.x + other.x, self.y + other.y, self.z + other.z)
        elif isinstance(other, Vector2):
            pos.set(self.x + other.x, self.y, self.z + other.z)

        return pos