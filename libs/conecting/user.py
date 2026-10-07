from socket import socket
from hashlib import sha1
from typing import Any, Generator

from libs import GameDataToServerDTO, GameDataToClientDTO


def hash(password: str) -> str:
    return sha1(password.encode()).hexdigest()

class User:
    name: str
    password: str
    connect: socket | str | None
    user_action: list[GameDataToServerDTO]
    server_data: GameDataToClientDTO | None

    def __init__(self, name: str, password: str):
        self.name = name
        self.password = hash(password)
        self.connect = None
        self.user_action = []
        self.server_data = None

    def test_password(self, password: str) -> bool:
        return hash(password) == self.password

    def add_message(self, dto: GameDataToServerDTO):
        self.user_action.append(dto)

    def send_to_user(self, dto: GameDataToClientDTO):
        self.server_data = dto

    @property
    def get_user_action(self) -> Generator[GameDataToServerDTO, Any, None]:
        for i in self.user_action:
            yield i
        self.user_action = []

    @property
    def get_data_from_server(self) -> Generator[GameDataToClientDTO, Any, None]:
        if self.server_data:
            yield self.server_data
        self.server_data = None
