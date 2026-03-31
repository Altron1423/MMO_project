class Vector2:
    x: int
    z: int
    _vector_type_ = "Vector2"

    def __init__(self, *position):
        if len(position) > 2:
            raise TypeError("Vector2 only accepts two positions")
        if len(position) == 1 and type(position[0]) == str:
            self.from_string(position[0])
        else:
            self.set(*position)

    def set(self, *position):
        position = [*position] + [0] * (2 - len(position))
        self.x, self.z = position

    def from_string(self, data: str):
        if data[0] == '<' and data[-1] == '>':
            data = data[1:-1]
            tp, data = data.split(':')
            if tp != self._vector_type_:
                raise TypeError(f"This string not {self._vector_type_}")
            self.set(*list(map(int, data.split(','))))
        else:
            raise TypeError("Vector2 only accepts strings")

    def __mul__(self, other):
        v = Vector2()

        if isinstance(other, int):
            v.set(self.x * other, self.z * other)
        elif isinstance(other, float):
            v.set(int(self.x * other), int(self.z * other))
        elif isinstance(other, Vector2):
            v.set(self.x * other.x, self.z * other.z)

        return v

    def __add__(self, other):
        v = Vector2()

        if isinstance(other, int):
            v.set(self.x + other, self.z + other)
        elif isinstance(other, Vector2):
            v.set(self.x + other.x, self.z + other.z)

        return v

    def __str__(self):
        return f"<{self._vector_type_}:{self.x},{self.z}>"