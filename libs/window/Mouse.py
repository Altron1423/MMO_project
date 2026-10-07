import pygame as pg

from libs.math import Position2


class Mouse:
    class Screen:
        shift: Position2
        scale: int
        scaling: bool

        def __init__(self):
            self.shift = Position2(0, 0)
            self.scale = 1
            self.scaling = False

        def set_parameters(self, shift: Position2 = None, scale: int = None, scaling: bool = None):
            if shift is not None:
                self.shift = shift
            if scale is not None:
                self.scale = scale
            if scaling is not None:
                self.scaling = scaling

        def rescale(self, scale: int):
            self.scale = scale

        def move(self, position: Position2):
            self.shift = position

    mouse: pg.mouse
    absolute: Position2
    position_on_screen: Position2
    shift_main_screen: Position2
    scale: int
    address_data: dict[str, Screen]
    buttons: list

    def __init__(self):
        self.mouse = pg.mouse
        self.absolute = Position2(-1, -1)
        self.position_on_screen = Position2(-1, -1)
        self.shift_main_screen = Position2(0, 0)
        self.scale = 1
        self.address_data = {}
        self.buttons = []

    def set_absolute(self, position: Position2):
        self.absolute = position
        self.position_on_screen = (self.absolute - self.shift_main_screen) // self.scale

    def update_screen_data(self, shift_position: Position2, scale:int=None, address:str="main"):
        if address == "main":
            if scale is not None:
                self.scale = scale
            self.shift_main_screen = shift_position
        elif address in self.address_data.keys():
            self.address_data[address].move(shift_position)
            self.address_data[address].rescale(scale)

    def update(self):
        # self.mousePos2 = ((self.mousePos[0] - dx) // self.K_Mushtub, (self.mousePos[1] - dy) // self.K_Mushtub)
        if self.mouse.get_focused():
            self.set_absolute(self.__get_mouse_position__())
        else:
            self.set_absolute(Position2(-1, -1))

    def get_position(self, address_screen:str="main"):
        if address_screen == "main":
            position = self.position_on_screen
        elif address_screen in self.address_data.keys():
            scale = self.address_data[address_screen].scale
            shift = self.address_data[address_screen].shift
            position = (self.position_on_screen - shift) // scale
        else:
            position = Position2(-1,-1)

        return position

    def add_address(self, address, data):
        screen = self.Screen()
        screen.set_parameters(**data)
        self.address_data[address] = screen

    def add_button(self, button):
        if button is not None:
            self.buttons.append(button)

    def interactive(self, event):
        if event.type == 1025:
            self.select(event.button)
        elif event.type == 1026:
            self.unselect(event.button)
            self.un_hold()

    def select(self, button):
        ...

    def unselect(self, button):
        ...

    def un_hold(self):
        for button in self.buttons:
            button.un_hold()
        self.buttons = []

    def __get_mouse_position__(self):
        return Position2(*self.mouse.get_pos())
