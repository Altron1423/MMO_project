import pygame as pg

from libs.graphics.Bars import Bars
from libs.math import Size2, Position2, Recalc
from libs.window.Mouse import Mouse
from libs.graphics.TriggerGen import TriggerGen
from libs.graphics.interface_elements.buttons_element import Button
from libs.graphics.interface_elements.png_element import PngElement
from libs.graphics.interface_elements.text_element import TextElement
from libs.graphics.polygons import ManyPolygonizer


class ButtonManager:
    _buttons: list[Button]
    polygonizer: ManyPolygonizer
    mouse: Mouse
    last_polygonizer: ManyPolygonizer | None
    address: str
    surface: pg.Surface | None
    surface_size: Size2
    active_button: int | None
    dynamic_position_X: Bars
    dynamic_position_Y: Bars

    def __init__(self, mouse):
        self._buttons = []
        self.polygonizer = ManyPolygonizer(Size2(100, 100))
        self.mouse = mouse
        self.last_polygonizer = None
        self.address = "main"
        self.surface = None
        self.active_button = None
        self.dynamic_position_X = Bars(0, 0, 0)
        self.dynamic_position_Y = Bars(0, 0, 0)


    def set_surface(self, surface):
        self.surface = surface
        self.surface_size = Size2(surface.get_size())
        for button in self._buttons:
            button.set_surface_size(self.surface_size)

    def set_address(self, new_address):
        self.address = new_address

    def set_polygonizer(self, polygonizer: ManyPolygonizer):
        self.last_polygonizer = polygonizer

    def set_move_limit_x(self, lim):
        self.dynamic_position_X.setLimit(lim)

    def set_move_limit_y(self, lim):
        self.dynamic_position_Y.setLimit(lim)


    def add_button(self, text, position: Recalc, size: Recalc, triggers):
        button = self._create_button("button")
        button.set_text(text)
        button.set_button_position_size(position, size)
        button.set_triggers(triggers)
        return button

    def add_text(self, text, position: Recalc, size: Recalc):
        button: Button | PngElement | TextElement = self._create_button()
        button.set_type("txt")
        # log(text)
        button.set_text(text)
        button.set_button_position_size(position, size)
        # button.move_to(position[:2])
        # button.resize(position[2:])
        return button

    def add_png(self, position: Recalc, size: Recalc, png):
        button = self._create_button()
        button.set_type("png")
        # button.move_to(position[:2])
        # if len(position) == 2:
        #     button.resize(png.get_size())
        # else:
        #     button.resize(position[2:])
        if len(position) == 1:
            position = [*position, *png.get_size()]
        button.set_button_position_size(position, size)
        button.set_png(png)


        return button

    def add_png_but(self, position: Recalc, size: Recalc, triggers, png):
        button = self._create_button("png_but")
        # button.move_to(position[:2])
        # if len(position) == 2:
        #     button.resize([*png.get_size()])
        # else:
        #     button.resize(position[2:])
        # if len(position) == 1:
        #     position = [*position, *png.get_size()]

        button.set_button_position_size(position, size)
        button.set_png(png)
        button.set_triggers(triggers)

        return button

    def add_mower(self, position: Recalc, size: Recalc, moveX: None|Bars = None, moveY: None|Bars = None):
        button = self._create_button()
        button.set_type("mower")
        button.set_button_position_size(position, size)
        trigers = TriggerGen()

        if moveX is not None:
            mvX = moveX
            trigers.MWD(lambda x: moveX.add(-0.05 * moveX.getFull()[1]))
            trigers.MWU(lambda x: moveX.add(0.05 * moveX.getFull()[1]))
        else:
            mvX = None

        if moveY is not None:
            mvY = moveY
            trigers.MWD(lambda x: moveY.add(-0.05 * moveY.getFull()[1]))
            trigers.MWU(lambda x: moveY.add(0.05 * moveY.getFull()[1]))
        else:
            mvY = None

        button.set_triggers(trigers)
        button.set_mover(mvX, mvY)

    def key_press(self, key: int, key_type:int):
        ...


    def get_button(self, index):
        if index is not None:
            return self._buttons[index]
        return None

    def cleen_buttons(self):
        self._buttons = []

    def select(self, event):
        but = event.button
        up = event.type == pg.MOUSEBUTTONDOWN
        button: Button = self.get_button(self.active_button)
        if button is not None:
            button.select((but, up))

    def draw(self):
        if self.surface is not None:
            mouse_pos = self.mouse.get_position(self.address)
            if mouse_pos in self.surface_size:
                pass
            else:
                mouse_pos = Position2(-1000, 1000)
            self.active_button = self._testing_activ(mouse_pos)
            self.mouse.add_button(self.get_button(self.active_button))
            for i, butt in enumerate(self._buttons):
                butt.draw(self.surface, self.active_button == i)

    def _testing_activ(self, mouse_pos):
        last = None
        for i, butt in enumerate(self._buttons):
            if butt.test_active(mouse_pos):
                last = i
        return last

    def _create_button(self, type_button="button"):

        if type_button == "button":
            button = Button(self, len(self._buttons))
        elif type_button == "mower":
            button = Button(self, len(self._buttons))
        elif type_button == "png":
            button = PngElement(self, len(self._buttons))
        elif type_button == "txt":
            button = TextElement(self, len(self._buttons))
        elif type_button == "png_but":
            button = PngElement(self, len(self._buttons))
        else:
            raise ValueError

        self._buttons.append(
            button
        )

        if self.last_polygonizer is not None:
            button.set_polygonizer(self.last_polygonizer)
        else:
            button.set_polygonizer(self.polygonizer)

        if self.surface is not None:
            button.set_surface_size(self.surface_size)


        return button



if __name__ == "__main__":
    pass
    # BM = ButtonManager(None)
    # t = TriggerGen().LMD(lambda: print("LMD"))
    # t2 = TriggerGen().LMU(lambda: print("LMU"))
    # print(t.__dict__)
    # print(t2.__dict__)
    # t3 = t + t2
    # t += t2
    # print(t.__dict__)

    # print(t[(0, True)])
    # t.__get__(12,345)
