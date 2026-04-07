from pathlib import Path

import pygame as pg

from typing import Callable, Generator, Any

from libs.animator_controller.animation_pack import AnimationPack
from libs.animator_controller.entity_animator import EntityAnimator
from .entitys import ClientPlayer
from .. import GameDataToClientDTO, GameDataToServerDTO, loger
from ..ticker import Ticker, MainTicker
from ..loaders.animator_loader import animator_loader, entity_animator_loader
from ..math import Vector2
from ..window.screen import Window
from ..window.camera import Camera

L2 = 2 ** 0.5

class GameClient:
    camera: Camera
    ticker: Ticker

    get_data_from_server:  Callable[
        [], Generator[GameDataToClientDTO, Any, None]
    ]
    send_game_data: Callable[[GameDataToServerDTO], None]
    window: Window

    player: ClientPlayer

    def __init__(self, player_name:str):
        self.player = ClientPlayer(player_name)
        self.ticker = MainTicker

        path = Path.cwd()
        path_animator = path.joinpath("src/data/animators")

        animator_loader.load_from_dir(path_animator)
        loger.status("GameMain loaded complete")

    def set_game_data(
            self,
            get_data_from_server: Callable[
                [], Generator[GameDataToClientDTO, Any, None]
            ],
            send_game_data: Callable[[GameDataToServerDTO], None],
            window: Window
    ) -> None:
        self.get_data_from_server = get_data_from_server
        self.send_game_data = send_game_data
        self.window = window

        # default_player_animator = EntityAnimator(self.ticker.add_tick("player_animation"))
        #
        # col_base = 80
        # for name, color in [("stand", (1, 1, 1)), ("m_r", (1, 1, 0)), ("m_d", (1, 0, 1)), ("m_l", (0, 1, 1)), ("m_u", (0, 0, 1))]:
        #     animation_pack = AnimationPack()
        #     for i in range(1, 4):
        #         col = (color[0] * col_base * i, color[1] * col_base * i, color[2] * col_base * i)
        #         surf = pg.Surface((60, 60))
        #         surf.fill(col)
        #         animation_pack.add_surface(surf)
        #     animation_pack.set_size(self.player.collision * 2)
        #     default_player_animator.add_animation_pack(name, animation_pack)

        default_player_animator = entity_animator_loader.get("player_animator")
        default_player_animator.set_size(self.player.collision * 4)

        self.camera = Camera(window, self.player, default_player_animator)

    def key_press(self, key: str, key_down: bool):
        if pg.K_w == key:
            if key_down:
                self.player.raw_orientation.z -= 1
            else:
                self.player.raw_orientation.z += 1
        elif pg.K_s == key:
            if key_down:
                self.player.raw_orientation.z += 1
            else:
                self.player.raw_orientation.z -= 1
        elif pg.K_d == key:
            if key_down:
                self.player.raw_orientation.x += 1
            else:
                self.player.raw_orientation.x -= 1
        elif pg.K_a == key:
            if key_down:
                self.player.raw_orientation.x -= 1
            else:
                self.player.raw_orientation.x += 1

        if self.player.raw_orientation.x != 0 and self.player.raw_orientation.z != 0:
            self.player.orientation = Vector2(
                round(self.player.raw_orientation.x / L2,3),
                round(self.player.raw_orientation.z / L2, 3)
            )
        else:
            self.player.orientation = self.player.raw_orientation

    def start(self):
        _ = self.send_game_data
        loger.status("GameMain started")

    def draw(self):
        if self.player.map_block is not None:
            self.camera.set_new_target_position(self.player.position)
            self.camera.update()
            self.window.add_task_draw(1, (self.camera.get_surface(), (0, 0)))

    def main(self):
        for act in self.get_data_from_server():
            self.player.get_data_from_server(act.player)

        self.draw()

        dto = self.player.data_to_server()
        self.send_game_data(dto)
