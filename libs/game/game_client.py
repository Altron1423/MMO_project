import pygame as pg

from typing import Callable, Generator, Any
from .. import GameDataToClientDTO, GameDataToServerDTO, loger
from ..math import Position2, Vector2


class GameClient:
    get_data_from_server:  Callable[
        [], Generator[GameDataToClientDTO, Any, None]
    ]
    send_game_data: Callable[[GameDataToServerDTO], None]

    orientation: Vector2

    def __init__(self):
        self.orientation = Vector2(0, 0)
        loger.status("GameMain loaded complete")

    def set_game_data(
            self,
            get_data_from_server: Callable[
                [], Generator[GameDataToClientDTO, Any, None]
            ],
            send_game_data: Callable[[GameDataToServerDTO], None],
    ) -> None:
        self.get_data_from_server = get_data_from_server
        self.send_game_data = send_game_data

    def key_press(self, key: str, key_down: bool):
        if pg.K_w == key:
            if key_down:
                self.orientation.z = -1
            else:
                self.orientation.z = 0
        if pg.K_s == key:
            if key_down:
                self.orientation.z = 1
            else:
                self.orientation.z = 0
        if pg.K_d == key:
            if key_down:
                self.orientation.x = 1
            else:
                self.orientation.x = 0
        if pg.K_a == key:
            if key_down:
                self.orientation.x = -1
            else:
                self.orientation.x = 0


    def start(self):
        _ = self.send_game_data
        loger.status("GameMain started")

    def main(self):
        for act in self.get_data_from_server():
            loger.log(f"Client {act.position}")

        dto = GameDataToServerDTO(
            move=self.orientation,
            speed=1.0,
            target_position=Position2(0, 0),
            action="22"
        )
        self.send_game_data(dto)
