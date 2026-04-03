from libs.dtos import ClientPlayerDTO, GameDataToServerDTO, GameDataToClientDTO, PlayerLoadDTO
from libs.game.sub_classes import Inventory
from libs.game.entitys.entity import Entity
from libs.math import Position2


class Player(Entity):
    inventory: Inventory

    def __init__(self):
        super().__init__()
        self.inventory = Inventory()


    def set_changes_from_client(self, dto: GameDataToServerDTO):
        if abs(dto.move.x) + abs(dto.move.z) <= 1:
            self.orientation = dto.move
        self.speed_control = dto.speed

    def get_data_for_client(self) -> GameDataToClientDTO:
        dto = GameDataToClientDTO(
            map_block="",
            player=self.__player_data__,
            chunk_position=Position2(0, 0),
            position=self.position
        )
        return dto

    @classmethod
    def load_from_config(cls, dto: PlayerLoadDTO) -> "Player":

        player = super().load_from_config(dto)

        return player


    @property
    def __player_data__(self) -> ClientPlayerDTO:
        return ClientPlayerDTO(
            name=self.name,
            attributes=self.attributes.__dict__(),
            position=self.position,
            health=self.health,
            mana=self.mana,
            xp=self.xp,
            lvl=self.lvl,
            inventory=str(self.inventory),
        )

    def __copy__(self) -> "Player":
        player = super().__copy__()
        player.inventory = self.inventory
        return player
