import pygame as pg

from libs.graphics.Bars import Bars
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
    active_button: int | None
    dynamic_position_X: Bars
    dynamic_position_Y: Bars

    def __init__(self, mouse):
        self._buttons = []
        self.polygonizer = ManyPolygonizer([100, 100])
        self.mouse = mouse
        self.last_polygonizer = None
        self.address = "main"
        self.surface = None
        self.active_button = None
        self.dynamic_position_X = Bars(0, 0, 0)
        self.dynamic_position_Y = Bars(0, 0, 0)


    def set_surface(self, surface):
        self.surface = surface
        for button in self._buttons:
            button.set_surface_size(surface.get_size())

    def set_address(self, new_address):
        self.address = new_address

    def set_polygonizer(self, polygonizer: ManyPolygonizer):
        self.last_polygonizer = polygonizer

    def set_move_limit_x(self, lim):
        self.dynamic_position_X.setLimit(lim)

    def set_move_limit_y(self, lim):
        self.dynamic_position_Y.setLimit(lim)


    def add_button(self, text, position, triggers):
        button = self._create_button("button")
        button.set_text(text)
        button._set_p_s(position)
        # button.move_to(position[:2])
        # button.resize(position[2:])
        button.set_triggers(triggers)
        return button

    def add_text(self, text, position):
        button = self._create_button()
        button.set_type("txt")
        # log(text)
        button.set_text(text)
        button._set_p_s(position)
        # button.move_to(position[:2])
        # button.resize(position[2:])
        return button

    def add_png(self, position, png):
        button = self._create_button()
        button.set_type("png")
        # button.move_to(position[:2])
        # if len(position) == 2:
        #     button.resize(png.get_size())
        # else:
        #     button.resize(position[2:])
        if len(position) == 2:
            position = [*position, *png.get_size()]
        button._set_p_s(position)
        button.set_png(png)


        return button

    def add_png_but(self, position, triggers, png):
        button = self._create_button("png_but")
        # button.move_to(position[:2])
        # if len(position) == 2:
        #     button.resize([*png.get_size()])
        # else:
        #     button.resize(position[2:])
        if len(position) == 2:
            position = [*position, *png.get_size()]

        button._set_p_s(position)
        button.set_png(png)
        button.set_triggers(triggers)

        return button

    def add_mower(self, position, moveX: None|Bars = None, moveY: None|Bars = None):
        button = self._create_button()
        button.set_type("mower")
        button._set_p_s(position)
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
            if 0 <= mouse_pos[0] <= self.surface.get_size()[0] and 0 <= mouse_pos[1] <= self.surface.get_size()[1]:
                pass
            else:
                mouse_pos = [-1000, 1000]
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


        self._buttons.append(
            button
        )

        if self.last_polygonizer is not None:
            button.set_polygonizer(self.last_polygonizer)
        else:
            button.set_polygonizer(self.polygonizer)

        if self.surface is not None:
            button.set_surface_size(self.surface.get_size())


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
