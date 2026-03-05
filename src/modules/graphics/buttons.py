import time

import pygame as pg

from src.modules.graphics.polygons import Resizer, ManyPolygonizer, Polygon
from src.modules.loaders import ImageLoader
from src.modules.Bars import Bars
from src.modules import Mouse

# from src.data.Loger import log, log_step

if __name__ == "__main__":
    pg.init()

# ARIAL_25 = pg.font.SysFont('arial', 25)
KeysTransf = {
    pg.K_q: "q", pg.K_w: "w", pg.K_e: "e", pg.K_r: "r", pg.K_t: "t", pg.K_y: "y",
    pg.K_u: "u", pg.K_i: "i", pg.K_o: "o", pg.K_p: "p", pg.K_a: "a", pg.K_s: "s",
    pg.K_d: "d", pg.K_f: "f", pg.K_g: "g", pg.K_h: "h", pg.K_j: "j", pg.K_k: "k",
    pg.K_l: "l", pg.K_z: "z", pg.K_x: "x", pg.K_c: "c", pg.K_v: "v", pg.K_b: "b",
    pg.K_n: "n", pg.K_m: "m", pg.K_0: "0", pg.K_1: "1", pg.K_2: "2", pg.K_3: "3",
    pg.K_4: "4", pg.K_5: "5", pg.K_6: "6", pg.K_7: "7", pg.K_8: "8", pg.K_9: "9",
    pg.K_SPACE: " ", pg.K_COMMA: ",", pg.K_PERIOD: ".", pg.K_SLASH: "/", pg.K_MINUS: "-"
}



class TriggerGen:
    def __init__(self):
        self.triggers = {}
        self.last = None

    def LMD(self, function):
        self.triggers[(1, True)] = function
        return self

    def LMU(self, function):
        self.triggers[(1, False)] = function
        return self

    def RMD(self, function):
        self.triggers[(3, True)] = function
        return self

    def RMU(self, function):
        self.triggers[(3, False)] = function
        return self

    def MWD(self, function):
        self.triggers[(4, False)] = function
        return self

    def MWU(self, function):
        self.triggers[(5, False)] = function
        return self

    def HoldD(self, function):
        self.triggers[('hold', True)] = function
        return self

    def HoldU(self, function):
        self.triggers[('hold', False)] = function
        return self

    def key_down(self, key, function):
        self.triggers[(key, True)] = function
        return self

    def key_up(self, key, function):
        self.triggers[(key, False)] = function
        return self

    def __iadd__(self, other):
        if type(other) == dict:
            for k, f in other.items():
                self.triggers[k] = f
        elif isinstance(other, self.__class__):
            for k, f in other.triggers.items():
                self.triggers[k] = f
        return self

    def __getitem__(self, key):
        if key in self.triggers:
            self.last = key
            return self.triggers[key]
        return None


class Button(Resizer):
    manager: "ButtonManager"
    id: int
    polygons = ManyPolygonizer

    type: str | None
    triggers: TriggerGen | None

    text_polygon: Polygon | None
    png_polygon: Polygon | None

    visible: bool
    on: bool
    hold: bool
    holding: bool
    active: bool
    active_time: float | None
    active_delta: float
    description: str
    parameters: dict

    mvX: Bars | None
    mvY: Bars | None
    mouse_position_on_button: list[int] | None

    def __init__(self, manager, button_id):
        super().__init__([-1000, -1000], [10, 10])

        self.manager = manager
        self.id = button_id
        self.polygons = ManyPolygonizer(self.size)

        self.function_active = None

        self.type = None
        self.triggers = None

        self.text_polygon = None
        self.png_polygon = None

        self.visible = True
        self.on = True
        self.hold = False
        self.holding = False
        self.active = False
        self.active_time = False
        self.active_delta = 0.1
        self.description = ""
        self.parameters = {}

        self.mvX = self.mvY = None

    def get_parameters(self, name):
        return self.parameters.get(name)


    def set_parameters(self, name, parameters):
        self.parameters[name] = parameters

    def set_type(self, type_but: str):
        self.type = type_but

    def set_triggers(self, triggers):
        self.triggers = triggers
        self.function_active = self._active_rect

    def set_holding(self, holding):
        self.holding = holding

    def set_work(self, work):
        self.on = work

    def set_visible(self, visible):
        self.visible = visible

    def set_polygonizer(self, polygonizer):
        self.polygons = polygonizer.__copy__()
        if self.polygons.main_text is not None:
            self.text_polygon = self.polygons.get_polygon(self.polygons.main_text)
        if self.polygons.main_png is not None:
            self.png_polygon = self.polygons.get_polygon(self.polygons.main_png)

    def set_text(self, text):
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

    def set_mover(self, mvX: None|Bars, mvY: None|Bars):
        self.mvX = mvX
        self.mvY = mvY

    def set_dynamic_position(self):
        ...

    def set_percent_size(self, percent_size_x: float | None = None, percent_size_y: float | None = None):
        super().set_percent_size(percent_size_x, percent_size_y)
        self.polygons.set_surface_size(self.size)

    def resize(self, size):
        super().resize(size)
        self.polygons.set_surface_size(size)

    def set_surface_size(self, surface_size):
        super().set_surface_size(surface_size)
        self.polygons.set_surface_size(self.size)

    def _set_p_s(self, p_s):
        if type(p_s[0]) == float:
            self.set_percent_position(p_s[0])
        else:
            self.move_to([p_s[0], None])

        if type(p_s[1]) == float:
            self.set_percent_position(percent_position_y=p_s[1])
        else:
            self.move_to([None, p_s[1]])

        if type(p_s[2]) == float:
            self.set_percent_size(p_s[2])
        else:
            self.resize([p_s[2], None])

        if type(p_s[3]) == float:
            self.set_percent_size(percent_size_y=p_s[3])
        else:
            self.resize([None, p_s[3]])


    def _active_rect(self, mouse_position):
        return (
                        0 <= mouse_position[0] <= self.size[0] and
                        0 <= mouse_position[1] <= self.size[1]
                )

    def test_active(self, mouse_position: list[int]) -> bool:
        active = False
        mouse_position_on_button = [
            mouse_position[0] - self.position[0],
            mouse_position[1] - self.position[1]
        ]
        if self.on:
            if self.function_active is not None:
                active = self.function_active(mouse_position_on_button)
                if active:
                    self.mouse_position_on_button = mouse_position_on_button

            # if self.form == "rect":
            #     active = (
            #             0 <= mouse_position_on_button[0] <= self.size[0] and
            #             0 <= mouse_position_on_button[1] <= self.size[1]
            #     )
            # elif self.form == "circle":
            #     center_coordinate = [
            #         mouse_position_on_button[0] + self.size[0] // 2,
            #         mouse_position_on_button[1] + self.size[1] // 2
            #     ]
            #     active = center_coordinate[0] ** 2 + center_coordinate[1] ** 2 <= (self.size[0] // 2) ** 2

            if active and self.hold:
                self.active = True
                self.active_time = time.time() + self.active_delta
                # if self.active_time - time.time() > self.active_delta:
                #     self.active_time = time.time() + self.active_delta

        return active

    def select(self, trigger):
        if trigger[1] != self.hold:
            if self.triggers is not None:
                function = self.triggers[trigger]
                if function is not None:
                    function(self)
        self.hold = trigger[1]

    def un_hold(self):
        # function = self.triggers[('hold', False)]
        # if function is not None:
        #     function(self)
        self.hold = False

    def add_polygons(self, polygons):
        self.polygons += polygons

    def draw(self, surface, activ):
        if self.visible:
            # if self.type == "txt":
            #     status = 4
            # el
            if not self.on:
                status = 1
            elif self.active:
                status = 2
                if self.active_time <= time.time():
                    self.active = False
            elif activ:
                status = 3
            else:
                status = 4

            # option_rect = (*self.position, *self.size)
            # pg.draw.rect(surface, (100, 100, 100), option_rect)
            self.polygons.reset_status(status)
            # self.polygons._redraw()
            surface.blit(self.polygons.get_surf(), self.position)


        if self.on:
            if self.holding and self.hold and self.active:
                function = self.triggers[('hold', True)]
                if function is not None:
                    function(self)


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
        button = self._create_button()
        button.set_type("button")
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
        button = self._create_button()
        button.set_type("png_but")
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

    def _create_button(self):
        button = Button(self, len(self._buttons))
        self._buttons.append(
            button
        )

        if self.last_polygonizer is not None:
            button.set_polygonizer(self.last_polygonizer)
        else:
            button.set_polygonizer(self.polygonizer)

        if self.surface is not None:
            # log(self.surface.get_size())
            button.set_surface_size(self.surface.get_size())
            # log_step()
            # button.polygons.resize(button.size)


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
