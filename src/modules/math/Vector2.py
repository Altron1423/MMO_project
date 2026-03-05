class Vector2:
    x: int
    z: int

    def __init__(self, *position):
        self.set(*position)

    def set(self, *position):
        position += [0] * (2 - len(position))
        self.x, self.z = position

    def __mul__(self, other):
        pos = Vector2()

        if isinstance(other, int):
            pos.set(self.x * other, self.z * other)
        elif isinstance(other, Vector2):
            pos.set(self.x * other.x, self.z * other.z)

        return pos

    def __add__(self, other):
        pos = Vector2()

        if isinstance(other, int):
            pos.set(self.x + other, self.z + other)
        elif isinstance(other, Vector2):
            pos.set(self.x + other.x, self.z + other.z)

        return pos