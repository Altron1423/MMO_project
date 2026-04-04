from dataclasses import dataclass
from libs.math import Recalc, Vector2


@dataclass
class ButtonDTO:
    type: str
    polygons_name: str
    position: Recalc = Recalc()
    size: Recalc = Recalc(Vector2(1,1))
    text: str | None = None
    function: str | None = None
    png_name: str | None = None

@dataclass
class WindowDataDTO:
    recalc_position: Recalc
    recalc_size: Recalc
    default_polygonizer: str
    background: list[int] | None = None
    cord_new_button: list[int | float] | None = None

@dataclass
class WindowDTO:
    name: str
    data: WindowDataDTO
    buttons: list[ButtonDTO]
