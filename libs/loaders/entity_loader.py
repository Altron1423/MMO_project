import json
from pathlib import Path

from ..game import Player
from libs.loaders.loader import Loader
from libs.mappers.player import PlayerLoadMapper


class PlayerLoader(Loader):
    elements: dict[str, Player]

    def __init__(self):
        self.elements = {}

    def load(self, path: Path) -> None:
        with Path(path).open("r", encoding="utf-8") as file:
            json_data = json.load(file)
            if json_data["type"] in ["entity", "player"]:

                dto = PlayerLoadMapper.dict_to_dto(json_data["data"])
                player = Player.load_from_config(dto)

                self.add(player, dto.race)

    def load_from_dir(self, path: Path) -> None:
        for iPath in path.iterdir():
            self.load(iPath)

    def add(self, element: Player, name: str) -> None:
        self.elements[name] = element

    def get(self, name: str) -> Player | None:
        element = self.elements.get(name)
        return element

    def get_new(self, name: str) -> Player | None:
        element = self.elements.get(name).__copy__()
        return element


player_loader = PlayerLoader()
