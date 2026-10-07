from libs.window.screen import MainScreen as _MainScreen

class MainScreen(_MainScreen):
    ...

    def __init__(self, application):
        super().__init__(application)

    def append_single_saves(self, save_names:list[str]):
        self.window_manager.get_window("game_select").cleen_buttons()
        self.window_manager._append_buttons(save_names, "game_select")

    def append_online_saves(self, buttons:list[str]):
        self.window_manager.get_window("game_select").cleen_buttons()
        self.window_manager._append_buttons(buttons, "game_select")


