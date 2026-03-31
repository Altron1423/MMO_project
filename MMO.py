import pygame as pg

from libs import GameServer, GameClient, ConnectClientDTO
from libs.Core import CORE
from libs.conecting import ServerConnector, ClientConnector

pg.init()

from libs.save import SavesManager
from libs.application import Application

from libs.graphics.interface_elements.buttons_element import Button

class App(Application):
    save_manager:SavesManager = SavesManager()
    server_game: GameServer
    client_game: GameClient
    run_game: bool =False
    server: ServerConnector | ClientConnector | None
    save_selected: str | None = None
    user_data: ConnectClientDTO

    def __init__(self):
        super().__init__()

        config = {
            "open_single_player": [self.open_single_player, None],
            "open_game_menu": [self.open_game_menu, None],
            "save_select": [self.select_save, None],
        }
        game = {
            "start_game": [self.start_game, None],
        }
        test = {
            "test_function": [lambda bat: print(bat), None],
        }
        self.add_functions({
            "window": config,
            "game": game,
            "test": test
        })

        self.user_data = ConnectClientDTO(
            version=CORE.version,
            name="test",
            password="123"
        )
        self.server = None
        self.save_manager.set_path_save(self.path.joinpath(CORE.saves_directory))

    def key_press(self, key: str, key_down: bool):
        self.client_game.key_press(key, key_down)

    def run_more(self):
        if self.run_game:
            self.server.main(self.tick)
            self.server_game.main()
            self.client_game.main()

    def open_single_player(self, bat: Button):
        wm = self.main_screen.window_manager
        self.save_manager.load_from_dir()
        self.main_screen.append_single_saves(self.save_manager.get_saves_name())
        wm.set_main_window("game_select")
        wm.open_window("single_saves")

    def open_game_menu(self, bat: Button):
        wm = self.main_screen.window_manager
        wm.set_main_window("main_menu")
        wm.close_window("single_saves")

    def select_save(self, bat: Button):
        self.save_selected = bat.text_polygon.text

    def start_game(self, bat: Button):
        if self.save_selected is None:
            return

        self.server = ServerConnector(self.user_data)
        self.server.start_server()

        self.server_game = GameServer(self.user_data.name)
        self.server_game.set_game_data(
            self.save_manager.load_full_save(
                self.save_selected
            ),
            self.server.get_user_action,
            self.server.send_to_user
        )

        self.client_game = GameClient()
        self.client_game.set_game_data(
            self.server.get_data_from_server,
            self.server.send_game_data
        )

        self.run_game = True
        self.server_game.start()

    def exit(self, _=None):
        self.server.close()
        super().exit()



if __name__ == "__main__":
    game = App()
    game.run()
