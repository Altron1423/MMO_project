import time

from libs import Version, GameDataToServerDTO, GameDataToClientDTO, ConnectClientDTO
from libs.conecting import ServerConnector
from libs.math import Position2

if __name__ == '__main__':
    tick = 0
    server = ServerConnector(ConnectClientDTO(
        version=Version("0.1.0"),
        name="test",
        password="123"
    ))
    server.start_server()
    try:
        while True:
            tick += 1
            server.main(tick)
            time.sleep(0.05)
            for act, user_name in server.get_user_action():
                print(act.action)
                if act.action == "11":
                    print("Compressia!!!")
                    dto = GameDataToClientDTO(
                        map_block="",
                        chunk_position=Position2(0, 0),
                        position=Position2(2, 2)
                    )
                    server.send_to_user(dto, user_name)
                elif act.action == "22":
                    dto = GameDataToServerDTO(
                        move=(0.0, 0.0),
                        speed=1.0,
                        target_position=Position2(0, 0),
                        action="11"
                    )
                    server.send_game_data(dto)
                    dto = GameDataToClientDTO(
                        map_block="",
                        chunk_position=Position2(0, 0),
                        position=Position2(0, 0)
                    )
                    server.send_to_user(dto, user_name)
            for act in server.get_data_from_server():
                print(act)
    except KeyboardInterrupt:
        server.close()

