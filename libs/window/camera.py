import pygame as pg

from .screen import Window
from .. import MapPlate
from ..game import ClientEntity
from libs.animator_controller.entity_animator import EntityAnimator
from ..loaders.tile_map_loader import tile_map_loader
from ..math import Size2, Position2, Vector2


def rect(position: Position2, size: Size2) -> tuple[int, int, int, int]:
    return position.x, position.z, size.x, size.z

def get_sign(x: int | float) -> int:
    if x > 0:
        return 1
    elif x < 0:
        return -1
    return 0

def set_sign_from(to_sign: int, front_sign: int) -> int:
    return to_sign * get_sign(front_sign)

def get_name(map_plate: tuple[MapPlate, int] | None) -> str | None:
    if map_plate is not None and map_plate[0].layer == 2:
        return map_plate[0].texture
    return None

def gen_size_plates(start_plate: Position2, end_plate: Position2):
    for z in range(start_plate.z, end_plate.z + 1):
        for x in range(start_plate.x, end_plate.x + 1):
            yield Position2(x, z)

class Camera:
    window_plate_size: Size2
    window_plate_size_range: Size2
    center_pos: Position2

    count_plate_width: int = 12
    count_plate_height: int
    plate_size: Size2
    surface_size: Size2

    scale: float
    scaled_collision: Size2 = Size2(0, 0)
    save_zone: Size2

    surface: pg.Surface
    window: Window

    target_position: Position2
    position: Position2
    player: "Player"
    player_animator: EntityAnimator
    entities: dict[str, ClientEntity]
    was_new: bool = False

    first_plate: Position2
    end_plate: Position2
    map: list[
        list[
            None | tuple[
                MapPlate, int
            ]
        ]
    ]


    def __init__(self, window: Window, player: "Player", player_animator: EntityAnimator):
        self.window = window
        self.player = player
        self.entities = {}
        self.player_animator = player_animator
        self.player_animator.set_default_size(player.collision*4)
        self.target_position = self.position = player.position
        self.set_surface_size()
        self.save_zone = Size2(200, 200)

    def draw(self):
        shift = self.position * self.scale % self.plate_size
        # shift = Position2()
        for i_pos in gen_size_plates(self.first_plate, self.end_plate):
            pos = i_pos * self.plate_size - shift
            data = self.get_plate(i_pos)
            if data is not None:
                map_plate, height = data
                pos_plate_draw = rect(
                    pos,
                    self.plate_size
                )
                if map_plate.layer:
                    if map_plate.texture is not None:
                        pass
                    else:
                        pg.draw.rect(self.surface, map_plate.color, pos_plate_draw)

            pos_plate_draw = rect(
                self.plate_size // 2 + pos - 10,
                Size2(20, 20)
            )
            pg.draw.rect(self.surface, (255, 0, 0), pos_plate_draw, 2)

        for i_pos in gen_size_plates(self.first_plate, self.end_plate+1):
            data = self.get_tile(i_pos)
            if data[0][0] or data[0][1] or data[1][0] or data[1][1]:
                surf = tile_map_loader.get(data)
                pos = i_pos * self.plate_size - shift - self.plate_size // 2
                if surf is not None:
                    surf = pg.transform.scale(surf, self.plate_size.tuple)
                    self.surface.blit(surf, pos.tuple)
                else:
                    pos_plate_draw = rect(
                        pos,
                        self.plate_size
                    )
                    pg.draw.rect(self.surface, (255, 0, 0), pos_plate_draw, 2)

    def draw_entity(self, entity: ClientEntity):
        self.player_animator.set_type(
            self.player.preferential_orientation()
        )
        position = self.plate_size * self.center_pos + (entity.position - self.position) * self.scale
        surf = entity.animator.get_surface()
        if surf is not None:
            self.surface.blit(surf, (position - entity.scaled_collision*2).tuple)
        pg.draw.rect(self.surface, (0, 255, 0), rect(position - entity.scaled_collision, entity.scaled_collision *2), 5)

    def draw_entities(self):
        for name, entity in self.entities.items():
            if name != self.player.name:
                self.draw_entity(entity)

        self.player_animator.set_type(
            self.player.preferential_orientation()
        )

        position = self.plate_size * self.center_pos
        surf = self.player_animator.get_surface()
        if surf is not None:
            self.surface.blit(surf, (position - self.scaled_collision*2).tuple)
        pg.draw.rect(self.surface, (0, 255, 0), rect(position - self.scaled_collision, self.scaled_collision *2), 5)

    def get_surface(self):
        return self.surface

    def set_new_target_position(self, position: Position2):
        self.target_position = position

    def move_on(self) -> Position2:
        # move_on = Position2(
        #     self.target_position.x
        # )
        # x = self.target_position - self.position
        # zone = Position2(
        #     set_sign_from(self.save_zone.x, x.x),
        #     set_sign_from(self.save_zone.z, x.z)
        # )
        # if self.target_position - self.position < self.save_zone:
        # print(self.target_position - self.position, self.save_zone)
        move_on = self.target_position - self.position
        return move_on

    def update_map(self):
        self.map = [
            [None] * (self.window_plate_size_range.x + 2)
            for _ in range(self.window_plate_size_range.z + 2)
        ]

        first_plate = None
        end_plate = None

        for i_pos in Position2(-1, -1) + (self.window_plate_size_range + Vector2(1, 1)):

            plate_position = self.position + (i_pos - self.center_pos) * Vector2(50, 50)

            try:
                _, map_plate, height = self.player.__get_info_positon__(plate_position)
                if first_plate is None:
                    first_plate = i_pos
                end_plate = i_pos
                self.add_tile(i_pos, (map_plate, height))
            except:
                ...

        self.first_plate = first_plate
        self.end_plate = end_plate

    def update(self):
        self.position += self.move_on()

        if self.surface_size != self.window.surface_size:
            self.set_surface_size()
        self.surface.fill((0, 0, 0))

        if self.was_new:
            self.__update_entities__()
        self.update_map()
        self.draw()
        self.draw_entities()

    def add_tile(self, position: Position2, map_plate: tuple):
        position += 1
        self.map[position.z][position.x] = map_plate

    def get_plate(self, position: Position2) -> tuple[MapPlate, int] | None:
        position += 1
        return self.map[position.z][position.x]

    def get_tile(self, position: Position2) -> tuple[
        tuple[
            None | str, None | str
        ],
        tuple[
            None | str, None | str
        ]
    ]:
        position -= 1
        return (
            (get_name(self.get_plate(position                        )), get_name(self.get_plate(position+Position2(1, 0)))),
            (get_name(self.get_plate(position+Position2(0, 1))), get_name(self.get_plate(position+Position2(1, 1)))),
        )

    def set_surface_size(self):
        self.surface_size = self.window.surface_size
        self.surface = pg.Surface(self.surface_size.tuple)
        plate_size = self.surface_size.x // self.count_plate_width
        self.plate_size = Size2(plate_size, plate_size)
        self.count_plate_height = self.surface_size.z // plate_size + 1
        self.window_plate_size = Size2(self.count_plate_width, self.count_plate_height)
        self.window_plate_size_range = self.window_plate_size + 2
        self.scale = self.plate_size.x / 50
        self.center_pos = self.window_plate_size // 2

        # self.scale = 1
        # self.plate_size = Size2(50, 50)

        self.player_animator.set_scale(self.scale)
        self.__update_entities__()
        self.scaled_collision = self.player.collision * self.scale

    def __update_entities__(self):
        for _, entity in self.entities.items():
            entity.set_scale(self.scale)
