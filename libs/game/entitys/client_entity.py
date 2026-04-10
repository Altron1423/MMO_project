from libs.math import Position2, Vector2
from ... import EntityToClientDTO, entity_animator_loader
from .entity import Entity
from ...animator_controller import EntityAnimator


class ClientEntity(Entity):
    map_block_name: str
    target_position: Position2
    scaled_collision: Vector2
    last_direction_view: str
    animator: EntityAnimator

    def __init__(self, player_name: str):
        super().__init__()
        self.player_name = player_name
        self.animator = entity_animator_loader.get_new("player_animator")
        self.last_direction_view = 'down'
        self.scaled_collision = self.collision * 1

    def update_from_server(self, data: EntityToClientDTO):
        self.position = data.position
        self.health = data.health
        self.orientation = data.orientation
        self.animator.set_type(self.preferential_orientation)

    def set_scale(self, scale: float):
        self.animator.set_scale(scale)
        self.scaled_collision = self.collision * scale

    @property
    def preferential_orientation(self) -> str:
        return f"{self.type_action}_{self.direction_view}"

    @property
    def direction_view(self) -> str:

        if self.orientation.x > 0:
            self.last_direction_view = 'right'
        elif self.orientation.x < 0:
            self.last_direction_view = 'left'
        elif self.orientation.z > 0:
            self.last_direction_view = 'down'
        elif self.orientation.z < 0:
            self.last_direction_view = 'up'
        return self.last_direction_view

    @property
    def type_action(self) -> str:
        if self.orientation.x != 0 or self.orientation.z != 0:
            if self.speed_control > 1:
                return 'run'
            return 'walk'

        return 'idle'
