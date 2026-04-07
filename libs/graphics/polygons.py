import pygame as pg

from libs.Loger import loger
from libs.graphics.styler import Styler

from libs.math import Recalc, Size2, Position2, Vector2


class Resizer:
    position: Position2
    size: Size2
    recalc_position: Recalc
    recalc_size: Recalc
    surface_size: Size2 | None

    def __init__(self, recalc_position: Recalc, recalc_size: Recalc):
        # self.position = Position2()
        # self.size = Size2()

        self.surface_size = None
        self.set_recalc_position(recalc_position)
        self.set_recalc_size(recalc_size)

    def _recalculation_positions(self):
        if self.surface_size is not None:
            self.position = self.recalc_position.value(self.surface_size)

    def _recalculation_size(self):
        if self.surface_size is not None:
            self.size = self.recalc_size.value(self.surface_size)

    def set_surface_size(self, surface_size: Size2):
        self.surface_size = surface_size
        # loger.log(f"self.surface_size = {self.surface_size}")
        self._recalculation_size()
        self._recalculation_positions()

    def set_recalc_position(self, recalc_position: Recalc):
        self.recalc_position = recalc_position
        self._recalculation_positions()

    def set_recalc_size(self, recalc_size: Recalc):
        if isinstance(recalc_size, Recalc):
            self.recalc_size = recalc_size
        else:
            raise TypeError(f"{recalc_size} not {Recalc._type_}")
        self._recalculation_positions()


    def move_to(self, position: Position2):
        self.recalc_position = Recalc(Vector2(), position)

    def move_on(self, d_position: Position2):
        self.recalc_position += d_position

    def resize(self, new_size: Recalc):
        self.recalc_size = new_size


class Polygon(Resizer):
    id = 0

    type: int | None = None
    _png: pg.Surface | None = None
    _pngTr: pg.Surface | None = None
    _pngRect: pg.Rect | None = None

    _text: str | None = None
    option_surfaces: pg.Surface | None = None



    def __init__(self, position: Recalc, size: Recalc):
        super().__init__(position, size)
        self.styler = Styler()
        self._set_id()
        self.type = None

        self._png = None
        self._pngTr = None
        self._pngRect = None

        self._text = None
        self.option_surfaces = None

        self.border = False

    def draw(self, surface, status):
        option_rect = (*self.position.tuple, *self.size.tuple)
        if self.type is None:
            pass
        elif self.type == 1:
            color = self._get_color(status)
            if len(color) == 3:
                pg.draw.rect(surface, color, option_rect, self.border)
            else:
                sr = pg.Surface(self.size.tuple)
                sr.fill(color[:3])
                sr.set_alpha(color[3])
                surface.blit(sr, self.position)

        elif self.type == 2:
            if self._text is not None:
                surface.blit(self.option_surfaces, option_rect)

        elif self.type == 3:
            if self._png is not None:
                surface.blit(self._pngTr, option_rect)

    def set_style(self, style):
        self.styler = style
        self.option_surfaces = self.styler.text_render(self._text)


    def set_text(self, text:str):
        self._text = text
        # self.option_surfaces = self.styler.text_render(self.text)
        self.blit_text()

    def set_png(self, png):
        self._png = png
        self._resize_png()

    def resize(self, new_size):
        super().resize(new_size)
        self._resize_png()
        self.blit_text()

    def set_recalc_size(self, recalc: Recalc):
        super().set_recalc_size(recalc)
        self._resize_png()
        self.blit_text()

    def set_surface_size(self, surface_size):
        super().set_surface_size(surface_size)
        self._resize_png()
        self.blit_text()

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
        if self._png is not None:
            print(self._png, self.size.tuple)
            self._pngTr = pg.transform.scale(self._png, self.size.tuple)
            self._pngRect = self._png.get_rect(topleft=self.position)
        else:
            self._pngTr = None
            self._pngRect = None

    def _set_id(self):
        if not isinstance(self, DoterPolygon):
            self.id = Polygon.id
            Polygon.id += 1

    def blit_text(self):
        if self.surface_size is None:
            return
        surface = pg.Surface(self.surface_size.tuple, pg.SRCALPHA, 32)
        if self._text is not None:
            words = [word.split(' ') for word in self._text.splitlines()]
            space = self.styler.font.size(' ')[0]
            max_width, max_height = self.surface_size.x - 10, self.surface_size.z - 10
            x = y = 0
            word_width = word_height = 0
            for line in words:
                for word in line:
                    if word != "":
                        word_surface = self.styler.text_render(word)
                        word_width, word_height = word_surface.get_size()
                        if x + word_width >= max_width:
                            x = 0
                            y += word_height
                        surface.blit(word_surface, (x, y))
                        x += word_width + space
                    else:
                        x += space
                x = 0
                y += word_height
        self.option_surfaces = surface


    @classmethod
    def rect(cls, recalc_position:Recalc=None, recalc_size:Recalc=None):
        if recalc_position is None:
            recalc_position = Recalc()
        if recalc_size is None:
            recalc_size = Recalc()
        polygon = cls(recalc_position, recalc_size)
        polygon.type = 1
        return polygon

    @classmethod
    def text(cls, text, recalc_position:Recalc=None, recalc_size:Recalc=None):
        if recalc_position is None:
            recalc_position = Recalc()
        if recalc_size is None:
            recalc_size = Recalc()
        polygon = cls(recalc_position, recalc_size)
        polygon.type = 2
        polygon.set_text(text)
        return polygon

    @classmethod
    def png(cls, png, recalc_position:Recalc=None, recalc_size:Recalc=None):
        if recalc_position is None:
            recalc_position = Recalc()
        if recalc_size is None:
            recalc_size = Recalc()
        polygon = cls(recalc_position, recalc_size)
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
            from libs.loaders.image_loader import image_loader
            image = image_loader.get_image(data["pngName"])
            loger.log(image)
            polygon = Polygon.png(image)
        else:
            loger.log(f"ERROR TYPE {data['type']=}")
            raise

        if data.get("position") is not None:
            polygon.set_recalc_position(Recalc.load_from_str(data["position"]))
        if data.get("size") is not None:
            polygon.set_recalc_size(Recalc.load_from_str(data["size"]))

        if data.get("styleID") is not None:
            polygon.set_style(Styler.get(data["styleID"]))
        elif data.get("styleName") is not None:
            from libs.loaders.styler_loader import styler_loader
            polygon.set_style(styler_loader.get(data["styleName"]))
        if data.get("border") is not None:
           polygon.border = data["border"]

        return polygon


class DoterPolygon(Polygon):
    def __init__(self, main_polygon: Polygon):
        self.main_polygon = main_polygon
        super().__init__(main_polygon.recalc_position, main_polygon.recalc_size)
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
    def __init__(self, size: Size2):
        super().__init__(Recalc(), Recalc(Vector2(1,1)))
        self.polygons: list[Polygon] = []
        self.surface = pg.Surface(size.tuple)
        self.status = None
        self.last_status = None
        self.main_png = None
        self.main_text = None

    def _redraw(self):
        self.surface = pg.Surface(self.size.tuple, pg.SRCALPHA, 32)
        for polygon in self.polygons:
            polygon.draw(self.surface, self.status)

    def reset_status(self, status):
        self.status = status

    def set_surface_size(self, surface_size: Size2):
        super().set_surface_size(surface_size)
        # super().resize(size)
        for polygon in self.polygons:
            polygon.set_surface_size(surface_size)

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
        # loger.log(data['size'])
        many_polygon = cls(Size2())
        many_polygon.set_surface_size(Size2(data["size"]))
        # loger.log(many_polygon.__dict__)
        for i in data["polygons"]:
            polygon = Polygon.load_json(i)
            many_polygon.add_polygon(polygon)
        # loger.log(many_polygon.__dict__)
        return many_polygon


class DoterPolygons(ManyPolygonizer):
    def __init__(self, main_polygonizer):
        self.main_polygonizer = main_polygonizer
        super().__init__(Size2(10, 10))
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
