from libs.game.sub_classes import Attributer, Bar
from libs.math import Position2, Vector2


class Entity:
    attributes: Attributer
    name: None | str = None
    health: Bar
    position: Position2
    orientation: Vector2
    speed: float

    def __init__(self):
        self.attributes = Attributer()
        self.health = Bar()
        self.position = Position2()
        self.orientation = Vector2(1, 0)
        self.speed = 1

    def update(self):
        self.attributes.update()
        self.position += self.orientation * self.speed


