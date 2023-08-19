from threading import Thread
import socket


print(socket.SO_SNDBUF)


def work(i):
    udp_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    udp_socket.sendto(b"A" * 1, ("192.168.80.106", 6969))


for i in range(10000):
    Thread(target=work, args=(i,)).start()
