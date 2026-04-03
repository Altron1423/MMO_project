from pathlib import Path
from typing import Callable, Generator, Any

from . import GameStartException
from libs.save import SaveFull
from libs.generators import SaveCreateTest
from .entitys.player import Player
from .. import GameDataToClientDTO, GameDataToServerDTO, MapBlock
from ..Loger import loger
from ..loaders import map_loader
from ..loaders.entity_loader import player_loader
from ..math import Position2


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

    def __init__(self):
        path = Path.cwd()
        path_map = path.joinpath("src/data/map")
        path_player = path.joinpath("src/data/entities")

        map_loader.load_from_dir(path_map)
        player_loader.load_from_dir(path_player)

        loger.status("GameMain loaded complete")

        self.players = []
        self.players_in_game = {}



    def set_game_data(
            self, save_full: SaveFull,
            get_user_action: Callable[
                [], Generator[
                    tuple[GameDataToServerDTO, str],
                    Any, None
                ]
            ],
            send_to_user: Callable[[GameDataToClientDTO, str], None],
            player_name: str
    ) -> None:
        self.save = save_full
        if self.save.need_created():
            SaveCreateTest.create(self.save)
        self.get_user_action = get_user_action
        self.send_to_user = send_to_user
        self.summon_new_player(player_name)

    def summon_new_player(self, name: str) -> Player:
        player = player_loader.get_new("human")
        player.position = self.save.spawn_position+0
        player.map_block = self.save.spawn_map_block
        self.players.append(player)
        self.players_in_game[name] = player
        return player

    def start(self):
        if not self.save:
            raise GameStartException()
        loger.status("GameMain started")

    def main(self):
        for act, user_name in self.get_user_action():
            player = self.players_in_game[user_name]
            # loger.log(f"Server {user_name=} {act.move=}")

            player.set_changes_from_client(act)
            player.update()

            self.send_to_user(
                player.get_data_for_client(),
                user_name
            )

    def saving(self):
        self.save.saving()
        loger.status("GameMain saving")
