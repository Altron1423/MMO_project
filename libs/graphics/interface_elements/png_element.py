from libs.graphics.interface_elements.buttons_element import Button
from libs.graphics.polygons import Polygon
from libs.loaders.image_loader import ImageLoader


class PngElement(Button):

    png_polygon: Polygon | None

    def set_png(self, png):
        if type(png) == str:
            self.png_polygon.set_png(ImageLoader.get_image(png))
        elif type(png) == list:
            i = i2 = 0
            while i < len(png) and i2 < len(self.polygons.polygons):
                if self.polygons.polygons[i2].type == 3:
                    self.polygons.polygons[i2].set_png(ImageLoader.get_image(png[i]))
                    i += 1
                i2 += 1
        self.polygons._redraw()
