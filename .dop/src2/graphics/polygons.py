from __dop.src2.data.Loger import log
from __dop.src2.graphics.styler import Styler
# from src.data.loaders import StylerLoader, ImageLoader
from __dop.src2.data.loaders.styler_loader import styler_loader as StylerLoader
from __dop.src2.data.loaders.image_loader import image_loader as ImageLoader
import pygame as pg


class Resizer:
    def __init__(self, position, size):
        self.percent_use = [False, False, False, False]
        self.position = [*position].copy()
        self.size = [*size].copy()
        self.percent_position = [-1.0, -1.0]
        self.percent_size = [1.0, 1.0]
        self.surface_size = None

    def _recalculation_positions(self):
        if self.surface_size:
            if self.percent_use[0]:
                self.position[0] = int(self.surface_size[0] * self.percent_position[0])
            if self.percent_use[1]:
                self.position[1] = int(self.surface_size[1] * self.percent_position[1])

    def _recalculation_size(self):
        if self.surface_size:
            if self.percent_use[2]:
                self.size[0] = int(self.surface_size[0] * self.percent_size[0])
            if self.percent_use[3]:
                self.size[1] = int(self.surface_size[1] * self.percent_size[1])


    def set_surface_size(self, surface_size):
        self.surface_size = surface_size
        self._recalculation_size()
        self._recalculation_positions()

    def set_percent_position(self, percent_position_x: float | None = None, percent_position_y: float | None = None):
        if percent_position_x:
            self.percent_position[0] = percent_position_x
            self.percent_use[0] = True
        if percent_position_y:
            self.percent_position[1] = percent_position_y
            self.percent_use[1] = True
        self._recalculation_positions()

    def set_percent_size(self, percent_size_x: float | None = None, percent_size_y: float | None = None):
        if percent_size_x:
            self.percent_size[0] = percent_size_x
            self.percent_use[2] = True
        if percent_size_y:
            self.percent_size[1] = percent_size_y
            self.percent_use[3] = True
        self._recalculation_size()


    def move_to(self, position):
        position[0] = position[0] if position[0] else self.position[0]
        position[1] = position[1] if position[1] else self.position[1]
        self.position = position

    def move_on(self, d_position):
        position = (
            self.position[0] + d_position[0],
            self.position[1] + d_position[1]
        )
        self.move_to(position)

    def resize(self, new_size):
        new_size[0] = new_size[0] if new_size[0] else self.size[0]
        new_size[1] = new_size[1] if new_size[1] else self.size[1]
        self.size = new_size


class Polygon(Resizer):
    id = 0

    def __init__(self, position, size):
        super().__init__(position, size)
        self.styler = Styler()
        self._set_id()
        self.type = None

        self.png = None
        self.pngTr = None
        self.pngRect = None

        self.text = None
        self.option_surfaces = None

        self.border = False

    def draw(self, surface, status):
        option_rect = (*self.position, *self.size)
        if self.type is None:
            pass
        elif self.type == 1:
            color = self._get_color(status)
            pg.draw.rect(surface, color, option_rect, self.border)

        elif self.type == 2:
            if self.text is not None:
                surface.blit(self.option_surfaces, option_rect)

        elif self.type == 3:
            surface.blit(self.pngTr, option_rect)

    def set_style(self, style):
        self.styler = style

    def set_text(self, text:str):
        self.text = text
        self.option_surfaces = self.styler.text_render(self.text)

    def set_png(self, png):
        self.png = png
        self._resize_png()

    def resize(self, new_size):
        super().resize(new_size)
        self._resize_png()

    def set_percent_size(self, percent_size_x: float | None = None, percent_size_y: float | None = None):
        super().set_percent_size(percent_size_x, percent_size_y)
        self._resize_png()

    def set_surface_size(self, surface_size):
        super().set_surface_size(surface_size)
        self._resize_png()

    def __copy__(self):
        dp = DoterPolygon(self)
        return dp

    def _get_color(self, status):
        color = (3, 9, 200)
        match status:
            case 1:
                color = self.styler.color_off
            case 2:
                color = self.styler.color_clicked
            case 3:
                color = self.styler.color_select
            case 4:
                color = self.styler.color

        return color

    def _resize_png(self):
        if self.png is not None:
            self.pngTr = pg.transform.scale(self.png, self.size)
            self.pngRect = self.png.get_rect(topleft=self.position)
        else:
            self.pngTr = None
            self.pngRect = None

    def _set_id(self):
        if not isinstance(self, DoterPolygon):
            self.id = Polygon.id
            Polygon.id += 1


    @classmethod
    def rect(cls, position=[0,0], size=[0,0]):
        polygon = cls(position, size)
        polygon.type = 1
        return polygon

    @classmethod
    def text(cls, text, position=[0,0], size=[0,0]):
        polygon = cls(position, size)
        polygon.type = 2
        polygon.set_text(text)
        return polygon

    @classmethod
    def png(cls, png, position=[0,0], size=[0,0]):
        polygon = cls(position, size)
        polygon.type = 3
        polygon.set_png(png)
        return polygon

    @classmethod
    def load_json(cls, data:dict) -> "Polygon":
        """
        {"type": 1, "position": [0,0], "size": [0,0], "percent_position": [None,None], "percent_size": [None,None], "styleID": 0, "border": None, "text": None, "png": None}

        :param data: 
        :return: 
        """
        if data["type"] == 1:
            polygon = Polygon.rect()
        elif data["type"] == 2:
            polygon = Polygon.text(data.get("text"))
        elif data["type"] == 3:
            image = ImageLoader.get_image(data["pngName"])
            polygon = Polygon.png(image)
        else:
            log(f"ERROR TYPE {data['type']=}")

        if data.get("position") is not None:
            polygon.move_to(data["position"])
        if data.get("size") is not None:
            polygon.resize(data["size"])
        if data.get("percent_position") is not None:
            polygon.set_percent_position(*data["percent_position"])
        if data.get("percent_size") is not None:
            polygon.set_percent_size(*data["percent_size"])

        if data.get("styleID") is not None:
            polygon.set_style(Styler.get_styler(data["styleID"]))
        elif data.get("styleName") is not None:
            polygon.set_style(StylerLoader.get_styler(data["styleName"]))
        if data.get("border") is not None:
           polygon.border = data["border"]


        return polygon


class DoterPolygon(Polygon):
    def __init__(self, main_polygon):
        self.main_polygon = main_polygon
        super().__init__(main_polygon.position, main_polygon.size)
        self.id = main_polygon.id
        self.percent_position = None
        self.percent_size = None
        self.surface_size = None
        self.styler = None
        self.type = None
        self.border = None
        self.percent_use = None

    def __getattribute__(self, item):
        att = object.__getattribute__(self, item)
        if att is None:
            att = getattr(self.main_polygon, item)
        return att


class ManyPolygonizer(Resizer):
    def __init__(self, size):
        super().__init__([0,0], size)
        self.polygons: list[Polygon] = []
        self.surface = pg.Surface(self.size)
        self.status = None
        self.last_status = None
        self.main_png = None
        self.main_text = None

    def _redraw(self):
        self.surface = pg.Surface(self.size, pg.SRCALPHA, 32)
        for polygon in self.polygons:
            polygon.draw(self.surface, self.status)

    def reset_status(self, status):
        self.status = status

    def set_surface_size(self, size):
        super().set_surface_size(size)
        super().resize(size)
        # log(size)
        for polygon in self.polygons:
            polygon.set_surface_size(size)
            # log(polygon.__dict__)

        self._redraw()

    def add_polygon(self, polygon):

        self.polygons.append(polygon)
        polygon.set_surface_size(self.size)
        if polygon.type == 2:
            if self.main_text is None:
                self.main_text = polygon.id
        elif polygon.type == 3:
            if self.main_png is None:
                self.main_png = polygon.id


    def get_surf(self):
        if self.status != self.last_status:
            self.last_status = self.status
            self._redraw()
        return self.surface

    def get_polygon(self, id):
        for polygon in self.polygons:
            if polygon.id == id:
                return polygon

    def __iadd__(self, other):
        self.polygons += other.polygons

    def __copy__(self):
        return DoterPolygons(self)

    @classmethod
    def load_json(cls, data:dict) -> "ManyPolygonizer":
        """
        {"polygons": [], "size": [25, 25]}
        :param data:
        :return:
        """
        # log(data)
        many_polygon = cls(data['size'])
        for i in data["polygons"]:
            polygon = Polygon.load_json(i)
            many_polygon.add_polygon(polygon)

        return many_polygon


class DoterPolygons(ManyPolygonizer):
    def __init__(self, main_polygonizer):
        self.main_polygonizer = main_polygonizer
        super().__init__([10, 10])
        self.polygons = []
        for polygon in self.main_polygonizer.polygons:
            pl = polygon.__copy__()
            self.polygons.append(pl)

        self.surface = None
        self.status = None
        self.last_status = None

    def __getattribute__(self, item):
        att = object.__getattribute__(self, item)
        if att is None:
            att = getattr(self.main_polygonizer, item)
        return att
