from pathlib import Path

from libs.Loger import loger
from libs import SavesManager, GameServer


if __name__ == '__main__':

    game = GameServer()
    save_manager = SavesManager
    path = Path().cwd().joinpath("saves")
    save_manager.set_path_save(path)
    save_manager.load_from_dir()
    saves = save_manager.get_saves_name()
    loger.status(saves)
    save_full = save_manager.load_full_save(saves[0])
    game.set_game_save(save_full)
    game.start()
    game.saving()
    print("Test complit")

