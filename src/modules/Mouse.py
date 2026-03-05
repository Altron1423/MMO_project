from src.modules.Loger import loger

class Mouse:
    class Screen:
        def __init__(self):
            self.shift = (0, 0)
            self.scale = 1
            self.scaling = False

        def set_parameters(self, data):
            """
            {"shift": [0, 0], "scale": 1, "scaling": False}
            :param data:
            :return:
            """
            if "shift" in data:
                self.shift = data["shift"]
            if "scale" in data:
                self.scale = data["scale"]
            if "scaling" in data:
                self.scaling = data["scaling"]

        def rescale(self, scale):
            if scale is not None:
                self.scale = scale

        def move(self, x, y):
            self.shift = (x, y)

    def __init__(self, mouse):
        self.mouse = mouse
        self.absolute = (-1, -1)
        self.position_on_screen = (-1, -1)
        self.shift_main_screen = (0, 0)
        self.scale = 1
        self.address_data = {}
        self.buttons = []

    def set_absolute(self, position):
        self.absolute = position
        self.position_on_screen = (
            int(
                (position[0] - self.shift_main_screen[0]) / self.scale
            ),
            int(
                (position[1] - self.shift_main_screen[1]) / self.scale
            )
        )

    def update_screen_data(self, shift_x, shift_y, scale=None, address="main"):
        if address == "main":
            if scale is not None:
                self.scale = scale
            self.shift_main_screen = (shift_x, shift_y)
        elif address in self.address_data.keys():
            self.address_data[address].move(scale)
            self.address_data[address].rescale(scale)

    def update(self):
        # self.mousePos2 = ((self.mousePos[0] - dx) // self.K_Mushtub, (self.mousePos[1] - dy) // self.K_Mushtub)
        if self.mouse.get_focused():
            self.set_absolute(self.mouse.get_pos())
        else:
            self.set_absolute((-1, -1))

    def get_position(self, address_screen="main"):
        position = (-1, -1)
        if address_screen == "main":
            position = self.position_on_screen
        elif address_screen in self.address_data.keys():
            scale = self.address_data[address_screen].scale
            shift = self.address_data[address_screen].shift
            position = (
                int(
                    (self.position_on_screen[0] - shift[0]) / scale
                ),
                int(
                    (self.position_on_screen[1] - shift[1]) / scale
                )
            )

        return position

    def add_address(self, address, data):
        screen = self.Screen()
        screen.set_parameters(data)
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

