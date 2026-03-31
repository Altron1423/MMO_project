from libs import GameDataToServerDTO, GameDataToClientDTO
from libs.game.entitys.entity import Entity
from libs.math import Vector2, Position2


class Player(Entity):

    def __init__(self, player_name: str):
        super().__init__()
        self.player_name = player_name


    def set_changes_from_client(self, dto: GameDataToServerDTO):
        if abs(dto.move.x) + abs(dto.move.z) <= 1:
            self.orientation = dto.move
        self.speed = dto.speed


    def get_data_for_client(self) -> GameDataToClientDTO:
        dto = GameDataToClientDTO(
            map_block="",
            chunk_position=Position2(0, 0),
            position=self.position
        )
        return dto
