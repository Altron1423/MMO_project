from .Vector2 import Vector2
from .Size import Size2
from .Position import Position2

def test_eq_vector():
    assert Vector2(1, 2) == Vector2(1, 2)
    assert Size2(1, 2) == Size2(1, 2)
    assert Position2(1, 2) == Position2(1, 2)

def test_sum_vector_on_number():
    assert Vector2(1, 2) + 3 == Vector2(4, 5)
    assert Size2(1, 2) + 3 == Size2(4, 5)
    assert Position2(1, 2) + 3 == Position2(4, 5)

def test_sum_vector_on_vector():
    assert Vector2(1, 2) + Vector2(3, 4) == Vector2(4, 6)
    assert Size2(1, 2) + Size2(3, 4) == Size2(4, 6)
    assert Position2(1, 2) + Position2(3, 4) == Position2(4, 6)

def test_mul_vector_on_number():
    assert Vector2(1, 2) * 3 == Vector2(3, 6)
    assert Size2(1, 2) * 3 == Size2(3, 6)
    assert Position2(1, 2) * 3 == Position2(3, 6)


def test_mul_vector_on_vector():
    assert Vector2(1, 2) * Vector2(3, 4) == Vector2(3, 8)
    assert Size2(1, 2) * Size2(3, 4) == Size2(3, 8)
    assert Position2(1, 2) * Position2(3, 4) == Position2(3, 8)
