from typing import Any, Generator, Callable
import json

from libs import loger, GameDataToClientMapper

from libs.dtos import (
    ConnectServerDTO, ConnectClientDTO,
    GameDataToServerDTO, GameDataToClientDTO
)
from libs.mappers import (
    ConnectServerMapper,
    ConnectClientMapper,
    GameDataToServerMapper
)
from . import SocConnector, User
from socket import (
    socket,
    AF_INET, SOCK_STREAM, IPPROTO_TCP, TCP_NODELAY
)



class ServerConnector(SocConnector):
    access_external_connections: bool = False
    local_user: User
    users: list[User]

    external_connections: list[socket]
    current_users: list[tuple[str | socket, User]]

    connect_player: Callable[[str], Any]

    local_send_to_server_message: bytes
    local_send_to_client_message: bytes

    def __init__(self, dto: ConnectClientDTO):
        super().__init__(dto.version)
        self.external_connections = []
        self.local_user = User(dto.name, dto.password)
        self.current_users = [("localhost", self.local_user)]
        self.users = []
        self.local_send_to_server_message = b""
        self.local_send_to_client_message = b""

    def start_server(self):
        loger.status(f"Server starting on {self.LOCALHOST}")
        try:
            self.main_socket = socket(AF_INET, SOCK_STREAM)
            self.main_socket.setsockopt(IPPROTO_TCP, TCP_NODELAY, 1)
            self.main_socket.bind((self.LOCALHOST, self.server_port))
            self.main_socket.setblocking(False)
            self.main_socket.listen(5)
            loger.status(f"Server success start")
        except Exception as e:
            loger.error("Server startup error with exception:", e)

    def main(self, tick):
        if self.main_socket is None:
            return

        if tick % 40 and self.access_external_connections:
            try:
                new_socket, addr = self.main_socket.accept()
                # loger.log(f'New connect {addr=}, {new_socket=}')
                new_socket.setblocking(False)
                self.external_connections.append(new_socket)
            except BlockingIOError:
                pass

        for connect in self.external_connections:
            try:
                d = connect.recv(1024)
                # loger.log(f"Raw message in <external_connections>: {d}")
                data = self.decode_message(d, True)
                if data is None:
                    pass
                elif data == self.testing_server_message:
                    dto = ConnectServerDTO(
                        version=self.game_version,
                        name="qwerty"
                    )
                    self.__send_to__(
                        connect,
                        {self.true_server_testing: ConnectServerMapper.dto_to_dict(dto)},
                    )
                elif data == self.drop_connect:
                    self.__drop_connect__(connect)
                    loger.log(f"drop connect")
                else:
                    data = data.get(self.join_in_game_message)
                    if data is None:
                        continue
                    dto = ConnectClientMapper.dict_to_dto(data)
                    if dto.version:
                        user = self.__find_user__(dto.name)
                        if user is None:
                            user = self.__crate_user__(dto, connect)
                            correct = True
                        else:
                            correct = user.test_password(dto.password)

                        if correct:
                            self.current_users.append((connect, user))
                            self.external_connections.remove(connect)
                            self.connect_player(user.name)
                            self.__send_to__(connect, self.true_join_game)
                        else:
                            self.__send_to__(connect, self.false_join_game)
            except BlockingIOError:
                pass

        for connect, user in self.current_users:
            try:
                if type(connect) == socket:
                    d = connect.recv(1024)
                    # loger.log(f"Raw message in <current_users>: {d}")
                else:
                    d = self.local_send_to_server_message
                    self.local_send_to_server_message = b""
                if len(d) == 0:
                    raise BlockingIOError
                data = self.decode_message(d, True)
                if data is None:
                    pass
                elif data == self.drop_connect:
                    self.__drop_connect__(connect)
                    loger.log(f"drop connect")
                else:
                    status_dict = data.get(self.game_status_message)
                    if status_dict is not None:
                        dto = GameDataToServerMapper.dict_to_dto(status_dict)
                        user.add_message(dto)
            except BlockingIOError as e:
                ...
            except ConnectionAbortedError:
                self.__drop_connect__(connect)
            except ConnectionResetError:
                self.__drop_connect__(connect)

            for data in user.get_data_from_server:
                game_data = GameDataToClientMapper.dto_to_dict(data)
                self.__send_to__(connect, {self.game_status_message: game_data})

    def open_connection(self, connect_player: Callable[[str], Any]):
        self.access_external_connections = True
        self.connect_player = connect_player


    def get_user_action(self) -> Generator[tuple[GameDataToServerDTO, str], Any, None]:
        for _, user in self.current_users:
            for mes in user.get_user_action:
                yield mes, user.name

    def send_to_user(self, dto: GameDataToClientDTO, user_name: str):
        user = self.__find_user__(user_name)
        user.send_to_user(dto)


    def get_data_from_server(self) -> Generator[GameDataToClientDTO, Any, None]:
        if len(self.local_send_to_client_message):
            raw_server_message = self.decode_message(self.local_send_to_client_message)
            self.local_send_to_client_message = b""
            server_answer = raw_server_message.get(self.game_status_message)
            if server_answer is not None:
                yield GameDataToClientMapper.dict_to_dto(server_answer)

    def send_game_data(self, dto: GameDataToServerDTO):
        self.__local_to_server_send__({
            self.game_status_message: GameDataToServerMapper.dto_to_dict(dto)
        })


    def __send_to__(self, connect: socket | str, message: str | dict):
        if type(message) == dict:
            message = json.dumps(message)
        message = f"<{message}>".encode()
        if type(connect) == str:
            self.local_send_to_client_message = message
        else:
            connect.send(message)

    def __local_to_server_send__(self, message: str | dict):
        if type(message) == dict:
            message = json.dumps(message)
        self.local_send_to_server_message = f"<{message}>".encode()

    def __crate_user__(self, dto: ConnectClientDTO, connect: socket) -> User:
        user = User(dto.name, dto.password)
        user.connect = connect
        self.users.append(user)
        return user

    def __find_user__(self, name: str) -> User | None:
        if name == self.local_user.name:
            return self.local_user
        for user in self.users:
            if user.name == name:
                return user
        return None

    def __drop_connect__(self, connect: socket):
        if connect in self.external_connections:
            self.external_connections.remove(connect)
        else:
            for pair in self.current_users:
                if pair[0] == connect:
                    self.current_users.remove(pair)
                    break
        connect.close()

