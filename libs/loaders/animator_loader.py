from pathlib import Path

from . import Loader
from .entity_animator_loader import EntityAnimatorLoader, entity_animator_loader


class AnimatorLoader(Loader):
    player_loader: EntityAnimatorLoader = entity_animator_loader
    entity_animator_loader: EntityAnimatorLoader = entity_animator_loader


    @classmethod
    def load_from_dir(cls, path_map: Path) -> None:
        entity_animator_loader.load_from_dir(path_map.joinpath("players"))
        # entity_animator_loader.load_from_dir(path_map.joinpath("entities"))

animator_loader = AnimatorLoader()
