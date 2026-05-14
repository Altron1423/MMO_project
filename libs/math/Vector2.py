

class Vector2:
    x: int
    z: int
    _len_: float = 0
    _re_calc_: bool = False
    _vector_type_ = "Vector2"

    def __init__(self, *position):
        if len(position) > 2:
            raise TypeError(f"{self._vector_type_} only accepts two positions")
        if len(position) == 1:
            if type(position[0]) == str:
                self.from_string(position[0])
            elif type(position[0]) in [tuple, list]:
                self.set(*position[0])
        else:
            self.set(*position)

        self.__post_init__()
        self.__re_len__()

    def set(self, *position):
        if len(position) == 2:
            self.x = position[0]
            self.z = position[1]
        elif len(position) == 1:
            self.x = position[0]
            self.z = 0
        elif len(position) == 0:
            self.x = self.z = 0

    def from_string(self, raw_data: str):
        if raw_data[0] == '<' and raw_data[-1] == '>':
            data = raw_data[1:-1]
            tp, data = data.split(':')
            if tp != self._vector_type_:
                print(data)
                raise TypeError(f"This string not {self._vector_type_}")
            try:
                self.set(*list(map(int, data.split(','))))
            except:
                self.set(*list(map(float, data.split(','))))
        else:
            raise TypeError(f"{raw_data} only accepts strings for {self._vector_type_}")

    def __post_init__(self):
        ...

    def __re_len__(self):
        if self._re_calc_:
            self._len_ = (self.x ** 2 + self.z ** 2) ** 0.5

    def __len__(self):
        return self._len_

    def __mul__(self, other):
        v = self.__class__()

        if isinstance(other, int):
            v.set(self.x * other, self.z * other)
        elif isinstance(other, float):
            v.set(int(self.x * other), int(self.z * other))
        elif isinstance(other, (self.__class__, Vector2)):
            v.set(self.x * other.x, self.z * other.z)

        v.__re_len__()
        return v

    def __add__(self, other):
        v = self.__class__()

        if isinstance(other, int):
            v.set(self.x + other, self.z + other)
        elif isinstance(other, self.__class__):
            v.set(self.x + other.x, self.z + other.z)
        elif isinstance(other, Vector2):
            v.set(self.x + other.x, self.z + other.z)

        v.__re_len__()
        return v

    def __sub__(self, other):
        v = self.__class__()

        if isinstance(other, int):
            v.set(self.x - other, self.z - other)
        elif isinstance(other, self.__class__):
            v.set(self.x - other.x, self.z - other.z)
        elif isinstance(other, Vector2):
            v.set(self.x - other.x, self.z - other.z)

        v.__re_len__()
        return v

    def __mod__(self, other):
        v = self.__class__()

        if isinstance(other, int):
            v.set(self.x % other, self.z % other)
        elif isinstance(other, self.__class__):
            v.set(self.x % other.x, self.z % other.z)
        elif isinstance(other, Vector2):
            v.set(self.x % other.x, self.z % other.z)

        v.__re_len__()
        return v

    def __floordiv__(self, other):
        v = self.__class__()

        if isinstance(other, int):
            v.set(self.x // other, self.z // other)
        elif isinstance(other, self.__class__):
            v.set(self.x // other.x, self.z // other.z)

        v.__re_len__()
        return v

    def __truediv__(self, other):
        v = self.__class__()

        if isinstance(other, (int, float)):
            v.set(self.x / other, self.z / other)
        elif isinstance(other, self.__class__):
            v.set(self.x / other.x, self.z / other.z)

        v.__re_len__()
        return v

    def __str__(self):
        return f"<{self._vector_type_}:{self.x},{self.z}>"

    def __eq__(self, other):
        return self.x == other.x and self.z == other.z

    @property
    def tuple(self):
        return self.x, self.z


if __name__ == "__main__":
    v = Vector2(10, 20)
    print(v)
    print(v%3)
    print(v//3)

