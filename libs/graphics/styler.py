import pygame as pg


class Styler:
    id = 0
    stylers = []

    def __init__(self):
        self._set_id()
        self.color = (255, 0, 0)
        self.color_select = (0, 255, 0)
        self.color_clicked = (0, 0, 255)
        self.color_off = (0, 0, 0)
        self.font_color = (255, 255, 255)

        self.font_name = 'Comic Sans MS'
        self.font_size = 30
        self.font = pg.font.SysFont(self.font_name, self.font_size)

    def set_color(self, param, color):
        """
        0: color
        1: color_select
        2: color_clicked
        3: color_off
        4: font_color
        :param param:
        :param color:
        :return:
        """
        if color is not None:
            if param == 0:
                self.color = color
            elif param == 1:
                self.color_select = color
            elif param == 2:
                self.color_clicked = color
            elif param == 3:
                self.color_off = color
            elif param == 4:
                self.font_color = color

    def set_font(self, name: str | None = None, size: int | None = None):
        if name is not None:
            self.font_name = name
        if size is not None:
            self.font_size = size
        if name is not None or size is not None:
            self.font = pg.font.SysFont(self.font_name, self.font_size)

    def text_render(self, text):
        if text:
            return self.font.render(text, True, self.font_color)
        return None

    def _set_id(self):
        self.id = Styler.id
        Styler.id += 1
        Styler.stylers.append(self)

    @classmethod
    def load_json(cls, data:dict) -> "Styler":
        """
        {"colors": [None, None, None, None, None], "font": ['arial', 25]}
        :param data:
        :return:
        """
        style = Styler()
        for i in range(5):
            style.set_color(i, data["colors"][i])
        style.set_font(*data['font'])
        return style

    @classmethod
    def get_styler(cls, id) -> "Styler":
        return cls.stylers[id]

