from libs.math import Vector2


class Size2(Vector2):

    _vector_type_ = "Size"

    def __post_init__(self):
        if self.x < 0 or self.z < 0:
            raise TypeError("X and Z must be positive")

    # def __add__(self, other):
    #     super().__add__(other)
    #     pos = Size2()
    #
    #     if isinstance(other, int):
    #         pos.set(self.x + other, self.z + other)
    #     elif isinstance(other, Size2):
    #         pos.set(self.x + other.x, self.z + other.z)
    #     elif isinstance(other, Vector2):
    #         pos.set(self.x + other.x, self.z + other.z)

    def __contains__(self, item) -> bool:
        return 0 <= item.x <= self.x and 0 <= item.z <= self.z

    def __iter__(self):
        from libs.math import Position2
        for z in range(self.z):
            for x in range(self.x):
                yield Position2(x, z)
