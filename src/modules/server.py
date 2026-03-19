# import data.base as base
from platform import system
from socket import socket, AF_INET, SOCK_DGRAM, SOCK_STREAM, IPPROTO_TCP, TCP_NODELAY
from subprocess import check_output
import os
import scapy.all as sc


# import decon

# interface = decon.getting_interface(decon.getting_ip_of_this_device())
# print(local_ipv4())
class Adress_cheker:
    def __init__(self):
        self.local_ip = self.local_ipv4()
        self.ip_mac_network = {}

    def start(self) -> list:
        # self.local_ip = self.local_ipv4()
        if system() == "Windows":
            gateway = self.get_gateway_win()
        elif system() == 'Linux':
            if not os.getuid() == 0:
                print('\n[+] Запустите скрипт с правами суперпользователя!\n')
                return []
            gateway = self.get_gateway_linx()
        self.ip_mac_network = self.get_ip_mac_nework(
            f'{self.local_ip.split(".")[0]}.{self.local_ip.split(".")[1]}.{self.local_ip.split(".")[2]}.1/24')

        print(self.ip_mac_network)

        print(f'\n[+] Local IP: {self.local_ip}\n[+] Local Gateway: {gateway}')
        # print(ip_mac_network)
        self.print_ip_mac(self.ip_mac_network)
        return self.ip_mac_network


    def local_ipv4(self):
        st = socket(AF_INET, SOCK_DGRAM)
        try:
            st.connect(('10.255.255.255', 1))
            ip_l = st.getsockname()[0]
        except Exception:
            ip_l = '127.0.0.1'
        finally:
            st.close()
        return ip_l

    def get_gateway_win(self):
        # получаем адрес шлюза по умолчанию для текущего сетевого интерфейса
        com = f'route PRINT 0* | findstr {self.local_ipv4()}'.split()
        return check_output(com, shell=True).decode('cp866').split()[2]

    def get_gateway_linx(self):
        com = 'route -n'.split()
        ip_route = str(check_output(com, shell=True)).split("\\n")[2].split()[1].strip()
        if ip_route.isdigit():
            return ip_route
        else:
            sock = socket.gethostbyname(ip_route)
            return sock

    def get_ip_mac_nework(self, ip):
        answered_list = sc.srp(sc.Ether(dst='ff:ff:ff:ff:ff:ff') / sc.ARP(pdst=ip), timeout=1, verbose=True)[0]
        clients_list = []
        print(answered_list)
        for element in answered_list:
            clients_list.append({'ip': element[1].psrc, 'mac': element[1].hwsrc})
        return clients_list

    def print_ip_mac(self, mac_ip_list):
        print(f"\nMachine in Network:\n\nIP\t\t\t\t\tMAC-address\n{'-' * 41}")
        for client in mac_ip_list:
            print(f'{client["ip"]}\t\t{client["mac"]}')


class Server():

    def __init__(self):
        self.ad_cheker = Adress_cheker()
        self.LOCALHOST = self.ad_cheker.local_ip

    def start(self):
        print(self.LOCALHOST)
        mainSocket = socket(AF_INET, SOCK_STREAM)
        mainSocket.setsockopt(IPPROTO_TCP, TCP_NODELAY, 1)
        mainSocket.bind((self.LOCALHOST, 10000))
        mainSocket.setblocking(0)
        mainSocket.listen(5)

    def stop(self):
        pass

    def connect(self):
        pass

    def disconnect(self):
        pass

    def adress_check(self) -> list:
        return self.ad_cheker.start()

    def main(self):
        pass


if __name__ == "__main__":
    server = Server()
    data = server.adress_check()
    # print(data)


