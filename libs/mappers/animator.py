from dataclasses import dataclass

from ..math import Size2
from libs.dtos import (
    AnimationPackDataDTO, AnimatorDataDTO,
)


@dataclass(frozen=True, slots=True)
class AnimationPackDataMapper:

    @staticmethod
    def dto_to_dict(dto: AnimationPackDataDTO) -> dict[str, str]:
        return {
            "texture": dto.texture,
            "length": dto.length,
            "speed": dto.speed,
            "line": dto.line
        }

    @staticmethod
    def dict_to_dto(data: dict) -> AnimationPackDataDTO:
        return AnimationPackDataDTO(
            texture=data["texture"],
            length=data["length"],
            speed=data["speed"],
            line=data["line"]
        )

@dataclass(frozen=True, slots=True)
class AnimatorDataMapper:

    @staticmethod
    def dto_to_dict(dto: AnimatorDataDTO) -> dict[str, str]:
        animation_pack = {}
        animation_pack_data = dto.animation_pack
        for name_pack in animation_pack_data:
            animation_pack[name_pack] = AnimationPackDataMapper.dto_to_dict(animation_pack_data[name_pack])
        return {
            "name": dto.name,
            "size": str(dto.size),
            "animation_pack": animation_pack
        }

    @staticmethod
    def dict_to_dto(data: dict) -> AnimatorDataDTO:
        animation_pack = {}
        animation_pack_data = data["animation_pack"]
        for name_pack in animation_pack_data:
            animation_pack[name_pack] = AnimationPackDataMapper.dict_to_dto(animation_pack_data[name_pack])
        return AnimatorDataDTO(
            name=data["name"],
            size=Size2(data["size"]),
            animation_pack=animation_pack
        )
