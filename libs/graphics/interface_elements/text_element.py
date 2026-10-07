from libs.graphics.interface_elements.buttons_element import Button
from libs.graphics.polygons import Polygon


class TextElement(Button):

    text_polygon: Polygon | None

    def set_text(self, text: str | list[str]) -> None:
        if type(text) == str:
            self.text_polygon.set_text(text)
        elif type(text) == list:
            i = i2 = 0
            while i < len(text) and i2 < len(self.polygons.polygons):
                if self.polygons.polygons[i2].type == 2:
                    self.polygons.polygons[i2].set_text(text[i])
                    i += 1
                i2 += 1
        self.polygons._redraw()
