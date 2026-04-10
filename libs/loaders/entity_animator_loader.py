import json
import pygame as pg

from pathlib import Path

from libs import AnimatorDataMapper
from libs.loaders.loader import Loader
from .image_loader import image_loader

from ..ticker import MainTicker
from ..animator_controller import AnimationPack, EntityAnimator


class EntityAnimatorLoader(Loader):
    elements: dict[str, EntityAnimator]

    def load(self, path: Path) -> None:
        with Path(path).open("r", encoding="utf-8") as file:
            json_data = json.load(file)
            if json_data["type"] == "entity_animator":
                data = AnimatorDataMapper.dict_to_dto(json_data["data"])

                entity_animator = EntityAnimator(MainTicker.add_tick(data.name))

                for animation_pack_name in data.animation_pack:
                    animation_pack = AnimationPack()
                    ap_dto = data.animation_pack[animation_pack_name]
                    image = image_loader.get(ap_dto.texture)
                    line = -data.size.z * ap_dto.line

                    for i in range(ap_dto.length):
                        surf = pg.Surface(data.size.tuple, pg.SRCALPHA)
                        surf.blit(
                            image,
                            (
                                -data.size.x*i,
                                line
                            )
                        )
                        animation_pack.add_surface(surf)

                    animation_pack.set_time_to_surface(ap_dto.speed)
                    animation_pack.set_size(data.size)
                    entity_animator.add_animation_pack(animation_pack_name, animation_pack)

                entity_animator.set_default_size(data.size)
                self.add(entity_animator, data.name)

    def get(self, name: str) -> EntityAnimator | None:
        return super().get(name)

    def get_new(self, name: str) -> EntityAnimator | None:
        return super().get_new(name)


entity_animator_loader = EntityAnimatorLoader()
