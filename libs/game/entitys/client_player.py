from libs import GameDataToServerDTO, map_block_loader
from libs.dtos.player import ClientPlayerDTO
from libs.game.entitys.player import Player
from libs.math import Position2, Vector2


class ClientPlayer(Player):
    raw_orientation: Vector2
    map_block_name: str
    target_position: Position2
    last_direction_view: str

    def __init__(self, player_name: str):
        super().__init__()
        self.raw_orientation = Vector2(0, 0)
        self.player_name = player_name
        self.target_position = Position2()
        self.last_direction_view = 'down'

    def preferential_orientation(self) -> str:
        # if self.orientation.x > 0:
        #     self.type_orientation = 'walk_right'
        # elif self.orientation.x < 0:
        #     self.type_orientation = 'walk_left'
        # elif self.orientation.z > 0:
        #     self.type_orientation = 'walk_down'
        # elif self.orientation.z < 0:
        #     self.type_orientation = 'walk_up'
        # else:
        #     if self.type_orientation == 'walk_right':
        #         self.type_orientation = 'idle_right'
        #     elif self.type_orientation == 'walk_left':
        #         self.type_orientation = 'idle_left'
        #     elif self.type_orientation == 'walk_down':
        #         self.type_orientation = 'idle_down'
        #     elif self.type_orientation == 'walk_up':
        #         self.type_orientation = 'idle_up'

        # return self.type_orientation
        return f"{self.type_action}_{self.direction_view}"

    def get_data_from_server(self, dto: ClientPlayerDTO):
        self.name = dto.name
        self.position = dto.position
        self.health = dto.health
        self.mana = dto.mana
        self.xp = dto.xp
        self.lvl = dto.lvl
        self.map_block = map_block_loader.get(dto.map_block)

    def data_to_server(self) -> GameDataToServerDTO:
        return GameDataToServerDTO(
            move=self.orientation,
            speed=1.0,
            target_position=self.target_position,
            action="22"
        )

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
