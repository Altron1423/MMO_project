import pygame as pg

from typing import Callable, Generator, Any

from .entitys import ClientPlayer
from .. import GameDataToClientDTO, GameDataToServerDTO, loger
from ..math import Vector2
from ..window.screen import Window


class GameClient:
    get_data_from_server:  Callable[
        [], Generator[GameDataToClientDTO, Any, None]
    ]
    send_game_data: Callable[[GameDataToServerDTO], None]
    window: Window
    surface: pg.Surface

    player: ClientPlayer

    def __init__(self, player_name:str):
        self.player = ClientPlayer(player_name)
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
        self.surface = pg.Surface(window.surface.get_size())

    def key_press(self, key: str, key_down: bool):
        if pg.K_w == key:
            if key_down:
                self.player.orientation += Vector2(0, -1)
            else:
                self.player.orientation += Vector2(0, 1)
        elif pg.K_s == key:
            if key_down:
                self.player.orientation += Vector2(0, 1)
            else:
                self.player.orientation += Vector2(0, -1)
        elif pg.K_d == key:
            if key_down:
                self.player.orientation += Vector2(1, 0)
            else:
                self.player.orientation += Vector2(-1, 0)
        elif pg.K_a == key:
            if key_down:
                self.player.orientation += Vector2(-1, 0)
            else:
                self.player.orientation += Vector2(1, 0)


    def start(self):
        _ = self.send_game_data
        loger.status("GameMain started")

    def draw(self):
        self.surface.fill((0, 0, 0))
        pg.draw.rect(self.surface, (0, 0, 255), (15, 15, 75, 75),10)
        self.window.add_task_draw(1, (self.surface, (0, 0)))


    def main(self):
        for act in self.get_data_from_server():
            self.player.get_data_from_server(act.player)
            # loger.log(f"Client {act.position}")

        self.draw()

        dto = self.player.data_to_server()
        self.send_game_data(dto)
