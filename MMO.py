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
    server_game: GameServer | None = None
    client_game: GameClient | None = None
    run_game: bool = False
    server: ServerConnector | ClientConnector | None = None
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
            "start_game": [self.start_server_game, None],
            "leave_game": [self.leave_game, None]
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
        self.save_manager.set_path_save(self.path.joinpath(CORE.saves_directory))

    def key_press(self, key: str, key_down: bool):
        if self.client_game is not None:
            self.client_game.key_press(key, key_down)

    def run_more(self):
        if self.run_game:
            self.server.main(self.tick)
            self.server_game.main()
            self.client_game.main()

    def open_single_player(self, bat: Button=None):
        self.save_manager.load_from_dir()
        self.main_screen.append_single_saves(self.save_manager.get_saves_name())
        self.window_manager.set_main_window("game_select")
        self.window_manager.open_window("single_saves")

    def open_game_menu(self, bat: Button=None):
        self.window_manager.set_main_window("main_menu")
        self.window_manager.close_window("single_saves")

    def select_save(self, bat: Button=None):
        self.save_selected = bat.text_polygon._text

    def start_server_game(self, bat: Button=None):
        if self.save_selected is None:
            return

        self.server = ServerConnector(self.user_data)
        self.server.start_server()

        self.server_game = GameServer()
        self.server_game.set_game_data(
            self.save_manager.load_full_save(
                self.save_selected
            ),
            self.server.get_user_action,
            self.server.send_to_user,
            self.user_data.name
        )
        self.server.open_connection(
            self.server_game.summon_new_player,
        )

        self.client_game = GameClient(self.user_data.name)
        self.client_game.set_game_data(
            self.server.get_data_from_server,
            self.server.send_game_data,
            self.window_manager.get_window("main_game_screen")
        )

        self.server_game.start()
        self.client_game.start()
        self.run_game = True
        self.open_game_screen()

    def start_client_game(self, bat: Button=None):
        self.server = ClientConnector(self.user_data)
        self.server.start_client()

        self.client_game = GameClient(self.user_data.name)
        self.client_game.set_game_data(
            self.server.get_data_from_server,
            self.server.send_game_data,
            self.window_manager.get_window("main_game_screen")
        )

        self.client_game.start()
        self.run_game = True
        self.open_game_screen()

    def open_game_screen(self):
        self.window_manager.set_main_window("main_game_screen")
        self.window_manager.close_window("single_saves")

    def leave_game(self, bat: Button=None):
        self.run_game = False
        self.client_game = None
        if self.server_game is not None:
            self.server_game.saving()
            self.server_game = None
        self.server.close()
        self.server = None
        self.open_single_player()

    def exit(self, _=None):
        if self.server:
            self.server.close()
        if self.server_game:
            self.server_game.saving()
        super().exit()



if __name__ == "__main__":
    game = App()
    game.run()
