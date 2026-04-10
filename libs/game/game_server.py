from pathlib import Path
from typing import Callable, Generator, Any

from . import GameStartException
from libs.save import SaveFull
from libs.generators import SaveCreateTest
from .entitys.player import Player
from .. import GameDataToClientDTO, GameDataToServerDTO
from ..Loger import loger
from ..loaders.entity_loader import player_loader


class GameServer:
    save: SaveFull
    get_user_action:  Callable[
        [], Generator[
            tuple[GameDataToServerDTO, str],
            Any, None
        ]
    ]
    send_to_user: Callable[[GameDataToClientDTO, str], None]
    load_players: dict[str, Player]
    players_in_game: dict[str, Player]

    def __init__(self):
        path = Path.cwd()
        path_player = path.joinpath("src/data/entities")

        player_loader.load_from_dir(path_player)

        loger.status("GameMain loaded complete")

        self.load_players = {}
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
        player = self.load_players.get(name)
        if player is None:
            player = player_loader.get_new("human")
            player.transition_to(self.save.spawn_map_block)
            player.set_default(name, self.save.spawn_position)
            self.load_players[name] = player
        self.players_in_game[name] = player
        return player

    def start(self):
        if not self.save:
            raise GameStartException()
        loger.status("GameMain started")

    def main(self):
        for act, user_name in self.get_user_action():
            player = self.players_in_game[user_name]
            # loger.log(f"Server {user_name=} act.move={act.move}")

            player.set_changes_from_client(act)
            player.update()

            self.send_to_user(
                player.get_data_for_client(),
                user_name
            )
        self.save.update()

    def saving(self):
        self.save.saving()
        loger.status("GameMain saving")
