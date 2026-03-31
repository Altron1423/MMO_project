from pathlib import Path
from typing import Callable, Generator, Any

from . import GameStartException
from libs.save import SaveFull
from libs.generators import SaveCreateTest
from .entitys.player import Player
from .. import GameDataToClientDTO, GameDataToServerDTO
from ..Loger import loger
from ..loaders import map_loader


class GameServer:
    save: SaveFull
    get_user_action:  Callable[
        [], Generator[
            tuple[GameDataToServerDTO, str],
            Any, None
        ]
    ]
    send_to_user: Callable[[GameDataToClientDTO, str], None]
    players: list[Player]
    players_in_game: dict[str, Player]

    def __init__(self, player_name: str):
        path_map = Path.cwd().joinpath("src/data/map")

        map_loader.load_from_dir(path_map)

        loger.status("GameMain loaded complete")

        player = Player(player_name)

        self.players = [player]
        self.players_in_game = {player_name: player}

    def set_game_data(
            self, save_full: SaveFull,
            get_user_action: Callable[
                [], Generator[
                    tuple[GameDataToServerDTO, str],
                    Any, None
                ]
            ],
            send_to_user: Callable[[GameDataToClientDTO, str], None],
    ) -> None:
        self.save = save_full
        if self.save.need_created():
            SaveCreateTest.create(self.save)
        self.get_user_action = get_user_action
        self.send_to_user = send_to_user

    def start(self):
        if not self.save:
            raise GameStartException()
        loger.status("GameMain started")

    def main(self):
        for act, user_name in self.get_user_action():
            player = self.players_in_game[user_name]
            loger.log(f"Server {user_name=} {act=}")

            player.set_changes_from_client(act)
            player.update()

            self.send_to_user(
                player.get_data_for_client(),
                user_name
            )

    def saving(self):
        self.save.saving()