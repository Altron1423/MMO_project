from dataclasses import dataclass

from ..math import Size2


@dataclass
class AnimationPackDataDTO:
    texture: str
    length: int
    speed: int
    line: int

@dataclass
class AnimatorDataDTO:
    name: str
    size: Size2
    animation_pack: dict[str, AnimationPackDataDTO]
