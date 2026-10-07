from libs.save.map_chunk import MapChunk
from libs.math import Size2, Position2
from libs.dtos.entity import EntityToClientDTO


class MapBlock:
    id: int = 1

    size: Size2
    size_coordinate: Size2
    position: Position2
    name: str
    form: list[
        list[
            MapChunk | None
        ]
    ]
    players_in_game: list["Player"]
    players: dict[str, "Player"]
    enemies: list["Enemy"]
    entities_dto: list[EntityToClientDTO]
    entities_ranges: dict[tuple[str, str], int]

    def __init__(self, size: Size2, name: str):
        self.size = size
        self.size_coordinate = size * 50 * 16
        self.name = name
        self.position = Position2()
        self.id = 0
        self.form = []
        for z in range(size.z):
            self.form.append([None] * size.x)
        self.players_in_game = []
        self.players = {}
        self.enemies = []
        self.entities_dto = []
        self.entities_ranges = {}

    def set_form(self, form: list[list[MapChunk | None]]):
        for z in range(self.size.z):
            for x in range(self.size.x):
                self.form[z][x] = form[z][x]

    def set_chunk_on(
            self,
            chunk: MapChunk | None,
            position: Position2
    ) -> None:
        if position in self.size:
            self.form[position.z][position.x] = chunk

    def get_chunk(
            self,
            position: Position2,
    ) -> MapChunk:
        if position in self.size:
            return self.form[position.z][position.x]
        raise f"{position} not in {self.size}"

    def update(self):
        if len(self.players_in_game) == 0:
            return

        self.entities_dto = []
        self.entities_ranges = {}
        for player in self.players_in_game:
            self.entities_dto.append(
                player.get_light_data()
            )
        for enemy in self.enemies:
            self.entities_dto.append(
                enemy.get_light_data()
            )

        for entity_1 in self.entities_dto:
            for entity_2 in self.entities_dto:
                if entity_1 == entity_2:
                    continue
                elif (entity_2.name, entity_1.name) in self.entities_ranges:
                    continue
                x1, z1 = entity_1.position
                x2, z2 = entity_2.position
                self.entities_ranges[(entity_1.name, entity_2.name)] = abs(x1 - x2) + abs(z1 - z2)

    def get_near_entity(
            self, name: str, max_range: int
    ) -> dict[str, int]:
        entities_ranges = {}
        # max_range *= max_range
        for pair in self.entities_ranges:
            if name in pair:
                if self.entities_ranges[pair] <= max_range:
                    if pair[0] == name:
                        second_name = pair[1]
                    else:
                        second_name = pair[0]
                    entities_ranges[second_name] = self.entities_ranges[pair]
        return entities_ranges

    def get_entity_dto(self):
        return self.entities_dto

    def add_enemy(self, enemy: "Enemy"):
        enemy.map_block = self
        self.enemies.append(enemy)

    @property
    def Size(self):
        return self.size

    @Size.setter
    def Size(self, size: Size2):
        self.size = size
        self.size_coordinate = size * 50

    @property
    def Name(self):
        return self.name

    def __str__(self) -> str:
        return f"<{self.name}({self.id})>"

    def __copy__(self) -> "MapBlock":
        map_block = MapBlock(self.size, self.name)
        map_block.id = MapBlock.id
        MapBlock.id += 1
        map_block.__set_clone_form__(self.form)
        return map_block

    def __set_clone_form__(self, form: list[list[MapChunk | None]]) -> None:
        for x, z in self.size:
            if form[z][x] is not None:
                self.form[z][x] = form[z][x].__copy__()

