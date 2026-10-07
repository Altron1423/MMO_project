import json

import scapy.all as sc
from libs import Version, loger

from libs.dtos import AddressConnectDTO
from socket import (
    socket, gethostbyname, gethostname
)


class AddressChecker:
    def __init__(self, ip: str):
        self.local_ip = ip
        self.ip_mac_network = {}

    def start(self, output_info:bool=False) -> list:
        ip_list = self.local_ip.split(".")
        self.ip_mac_network = self.get_ip_mac_network(
            f'{ip_list[0]}.{ip_list[1]}.{ip_list[2]}.1/24', output_info
        )

        if output_info:
            self.print_ip_mac(self.ip_mac_network)
        return self.ip_mac_network

    @staticmethod
    def get_ip_mac_network(ip:str, verbose:bool=False) -> list[AddressConnectDTO]:
        answered_list = sc.srp(sc.Ether(dst='ff:ff:ff:ff:ff:ff') / sc.ARP(pdst=ip), timeout=1, verbose=verbose)[0]
        clients_list = []
        for element in answered_list:
            clients_list.append(
                AddressConnectDTO(
                    ip=element[1].psrc,
                    mac=element[1].hwsrc,
                )
            )
        return clients_list

    @staticmethod
    def print_ip_mac(mac_ip_list):
        print(f"\nMachine in Network:\n\nIP\t\t\t\t\tMAC-address\n{'-' * 41}")
        for client in mac_ip_list:
            print(f'{client["ip"]}\t\t{client["mac"]}')


class SocConnector:
    ad_checker: AddressChecker
    game_version: Version
    LOCALHOST: str
    main_socket: socket | None = None
    server_port: int = 10000
    testing_server_message: str = "WAY_IC"
    true_server_testing: str = "YIS"
    drop_connect: str = "COM_DROP"
    join_in_game_message: str = "COM_JOIN"
    true_join_game: str = "JOIN_TRUE"
    false_join_game: str = "JOIN_FALSE"
    game_status_message: str = "GAME_STATUS"
    server_close: str = "CLOSE"

    def __init__(self, version: Version):
        self.game_version = version
        self.LOCALHOST = self.local_ipv4()
        self.ad_checker = AddressChecker(self.LOCALHOST)

    @staticmethod
    def local_ipv4():
        ip_l = gethostbyname(gethostname())
        return ip_l

    def close(self):
        if self.main_socket is not None:
            self.main_socket.close()
            self.main_socket = None

    @staticmethod
    def decode_message(raw_message: bytes | str, string=False):
        if type(raw_message) == bytes:
            raw_message = raw_message.decode()
        # loger.log(f"{raw_message=}")
        # last = raw_message.find(">")
        last = -1
        if len(raw_message) and raw_message[0] == '<' and raw_message[last] == '>':
            message = raw_message[1:last]
            try:
                return json.loads(message)
            except json.decoder.JSONDecodeError as e:
                if string:
                    return message
            return None
        else:
            return None

    def __send__(self, message: str | dict) -> None:
        if self.main_socket is None:
            return
        if type(message) == dict:
            message = json.dumps(message)
        self.main_socket.send(f"<{message}>".encode())

    def __receive__(self) -> bytes:
        return self.main_socket.recv(1024)
