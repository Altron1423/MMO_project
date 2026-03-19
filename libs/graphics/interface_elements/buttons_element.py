import time

import pygame as pg

from libs.graphics.TriggerGen import TriggerGen
from libs.graphics.polygons import Resizer, ManyPolygonizer, Polygon
from libs.graphics.Bars import Bars

# from src.data.Loger import log, log_step

if __name__ == "__main__":
    pg.init()



class Button(Resizer):
    manager: "ButtonManager"
    id: int
    polygons = ManyPolygonizer

    type: str | None
    triggers: TriggerGen | None

    text_polygon: Polygon | None

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

        # self.type = "button"
        self.triggers = None

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

    # def set_type(self, type_but: str):
    #     self.type = type_but

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

    def set_text(self, text: str):
        if type(text) == str:
            self.text_polygon.set_text(text)
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

