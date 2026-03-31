import time
from typing import Any, Generator

from libs import loger
from libs.dtos import (
    AddressConnectDTO, ConnectServerDTO, ConnectClientDTO,
    GameDataToServerDTO, GameDataToClientDTO
)
from libs.mappers import ConnectServerMapper, ConnectClientMapper, GameDataToServerMapper, GameDataToClientMapper
from . import SocConnector

from socket import (
    socket,
    AF_INET, SOCK_STREAM, IPPROTO_TCP, TCP_NODELAY
)


class ClientConnector(SocConnector):
    connect_data: ConnectClientDTO | None = None
    data_from_server: GameDataToClientDTO | None = None

    def __init__(self, dto: ConnectClientDTO):
        super().__init__(dto.version)
        self.connect_data = dto

    def start_client(self):
        self.main_socket = socket(AF_INET, SOCK_STREAM)
        self.main_socket.setsockopt(IPPROTO_TCP, TCP_NODELAY, 1)

    def set_data(self, dto: ConnectClientDTO):
        self.game_version = dto.version
        self.connect_data = dto

    def main(self, tick: int=None):
        try:
            raw_server_message: dict = self.decode_message(
                self.__receive__()
            )
            if raw_server_message is not None:
                server_answer = raw_server_message.get(self.game_status_message)
                if server_answer is not None:
                    dto = GameDataToClientMapper.dict_to_dto(server_answer)
                    self.data_from_server = dto

        except BlockingIOError:
            pass


    def connect(self, address: AddressConnectDTO) -> None:
        loger.log(f"Connect to {(address.ip, self.server_port)}")
        self.main_socket.connect((address.ip, self.server_port))

    def disconnect(self):
        self.__send__(self.drop_connect)

    def close(self):
        self.disconnect()
        super().close()


    def get_data_from_server(self) -> Generator[GameDataToClientDTO, Any, None]:
        if self.data_from_server is not None:
            d = self.data_from_server
            self.connect_data = None
            yield d

    def send_game_data(self, dto: GameDataToServerDTO):
        self.__send__({
            self.game_status_message: GameDataToServerMapper.dto_to_dict(dto)
        })


    def join_game(self):
        if self.connect_data is not None:
            self.__send__({
                self.join_in_game_message: ConnectClientMapper.dto_to_dict(self.connect_data)
            })
            print(self.__receive__())

    def find_servers(self) -> list[AddressConnectDTO]:
        address_list = self.ad_checker.start()
        servers_list = []
        if len(address_list) > 0:
            self.start_client()
            for address in address_list:
                if self.__testing_is_server__(address):
                    servers_list.append(address)
                    # print("stop")
                    time.sleep(0.5)
            self.close()
        return servers_list


    def __testing_is_server__(self, address:AddressConnectDTO) -> ConnectServerDTO | None:
        answer = None
        try:
            self.connect(address)
            self.__send__(self.testing_server_message)

            raw_server_answer:dict = self.decode_message(
                self.__receive__()
            )
            # print(raw_server_answer)
            server_answer = raw_server_answer.get(self.true_server_testing)
            if server_answer is not None:
                dto = ConnectServerMapper.dict_to_dto(server_answer)
                if dto.version != self.game_version:
                    pass
                else:
                    answer = dto
            self.disconnect()
        except ConnectionRefusedError:
            pass
        except PermissionError:
            pass
        except OSError:
            pass

        return answer
