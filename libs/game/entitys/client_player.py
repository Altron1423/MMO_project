from libs import GameDataToServerDTO
from libs.dtos.player import ClientPlayerDTO
from libs.game.entitys.player import Player
from libs.math import Position2


class ClientPlayer(Player):
    map_block_name: str
    target_position: Position2

    def __init__(self, player_name: str):
        super().__init__()
        self.player_name = player_name
        self.target_position = Position2()

    def get_data_from_server(self, dto: ClientPlayerDTO):
        self.name = dto.name
        self.position = dto.position
        self.health = dto.health
        self.mana = dto.mana
        self.xp = dto.xp
        self.lvl = dto.lvl

    def data_to_server(self) -> GameDataToServerDTO:
        return GameDataToServerDTO(
            move=self.orientation,
            speed=1.0,
            target_position=self.target_position,
            action="22"
        )

