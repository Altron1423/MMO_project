import time

from libs import Version, GameDataToServerDTO, ConnectClientDTO, AddressConnectDTO
from libs.conecting import ClientConnector
from libs.math import Position2

if __name__ == '__main__':

    server = ClientConnector(ConnectClientDTO(
        version=Version("0.1.0"),
        name="test",
        password="123"
    ))
    servers = server.find_servers()
    # print(servers)
    server.start_client()
    ser = servers[0]
    server.connect(ser)

    # server.set_data(ConnectClientDTO(
    #     version=Version("0.1.0"),
    #     name="test",
    #     password="123"
    # ))
    time.sleep(0.1)
    server.join_game()


    dto = GameDataToServerDTO(
        move=(0.0, 0.0),
        speed=1.0,
        target_position=Position2(0, 0),
        action="22"
    )
    time.sleep(0.1)
    server.send_game_data(dto)

    tf = True
    try:
        while tf:
            server.main()
            time.sleep(0.05)
            for act in server.get_data_from_server():
                print(act)
                tf = False

    except KeyboardInterrupt:
        server.close()

    time.sleep(0.1)
    server.close()
