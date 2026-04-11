from libs import MapBlock, MapPlate, EntityToClientDTO
from libs.game.sub_classes import Attributer, ProgressBar
from libs.game.sub_classes.progress_bar import TriggersDTO
from libs.math import Position2, Vector2

def get_sign(x: int | float) -> int:
    if x > 0:
        return 1
    elif x < 0:
        return -1
    return 0

class Entity:
    name: None | str
    race: None | str

    attributes: Attributer
    health: ProgressBar
    mana: ProgressBar

    xp: ProgressBar
    raising_xp: float
    xp_boost: float
    lvl: int

    map_block: MapBlock | None = None
    position: Position2
    orientation: Vector2
    speed_control: float
    speed: float

    collision: Vector2
    step_height: int

    def __init__(self):
        self.name = None
        self.race = None
        self.attributes = Attributer()
        self.health = ProgressBar()
        self.mana = ProgressBar()

        self.xp = ProgressBar(unlimit=True)
        self.xp.set_triggers(TriggersDTO(
            _limit=self.__lvl_up__
        ))
        self.raising_xp = 1.05
        self.xp_boost = 1
        self.lvl = 1

        self.position = Position2()
        self.orientation = Vector2(0, 0)
        self.speed_control = 1
        self.speed = 8

        collision = 46
        self.collision = Vector2(collision // 2, collision // 2)
        self.step_height = 10

    def add_xp(self, xp: int) -> None:
        self.xp += int(xp * self.xp_boost)

    def update(self):
        self.attributes.update()
        self.__move__()

    def transition_to(self, map_block: MapBlock):
        if self.map_block is not None:
            self.transition_from()
        self.map_block = map_block
        map_block.players_in_game.append(self)
        self.map_block.players[self.name] = self
        self.position = Position2(150, 150)

    def transition_from(self):
        self.map_block.players_in_game.remove(self)
        self.map_block.players.pop(self.name)

    def disconnect(self):
        self.map_block.players_in_game.remove(self)

    def connect(self):
        self.map_block.players_in_game.append(self)

    def get_light_data(self) -> EntityToClientDTO:
        return EntityToClientDTO(
            self.name,
            self.position,
            self.health,
            self.orientation,
            "idle"
        )

    def __move__(self):
        move_on = self.orientation * self.speed * self.speed_control
        start_plate, start_heigh = self.__get_info_positon__(self.position)
        for i in (Vector2(1, 0), Vector2(0, 1)):
            move_on_1d = move_on * i
            if move_on_1d.x != 0 or move_on_1d.z != 0:
                if move_on_1d.x != 0:
                    collision = self.collision * i * get_sign(move_on_1d.x)
                else:
                    collision = self.collision * i * get_sign(move_on_1d.z)
                new_position = self.position + move_on_1d + collision
                if not new_position in self.map_block.size_coordinate:
                    continue
                new_plate, new_heigh = self.__get_info_positon__(new_position)
                if abs(new_heigh - start_heigh) <= self.step_height:
                    self.position += move_on_1d

        # print(self.map_block.name, start_plate.name, self.position)

    def __get_info_positon__(self, pos: Position2 = None) -> tuple[MapPlate, int]:
        if pos is None:
            pos = self.position
        chunk_size = 50
        position_chunk = pos // chunk_size // 16
        position_plate = pos // chunk_size % 16
        chunk = self.map_block.get_chunk(position_chunk)
        return chunk.get_plate(position_plate), chunk.get_height(position_plate)

    def __lvl_up__(self) -> None:
        quantity, max_xp = self.xp.get_full(True)
        quantity -= max_xp
        max_xp = int(max_xp * self.raising_xp)
        self.xp.update(quantity, max_xp)
        self.lvl += 1

    @classmethod
    def load_from_config(cls, dto) -> "Entity":
        entity = cls()
        entity.race = dto.race
        entity.attributes.load(dto.attributes)
        entity.xp.set_limit(dto.to_first_lvlup)
        entity.raising_xp = dto.raising_xp
        entity.xp_boost = dto.xp_boost
        return entity

    def __copy__(self):
        to = self.__class__()
        to.name = self.name
        to.race = self.race
        to.attributes = self.attributes
        to.health = self.health.__copy__()
        to.mana = self.mana.__copy__()
        to.xp = self.xp.__copy__()
        to.raising_xp = self.raising_xp
        to.lvl = self.lvl
        to.position = self.position
        to.orientation = self.orientation
        to.speed = self.speed

        return to
