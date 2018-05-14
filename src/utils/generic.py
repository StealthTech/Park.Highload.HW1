import os
import socket


def print_prefix(data, prefix='[SERVER]'):
    print('{} {}'.format(prefix, data))


def get_socket(ip_addr, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((ip_addr, port))
    sock.listen(50)
    sock.setblocking(0)
    return sock


def cpu_scale_fork(count):
    for _ in range(1, count):
        pid = os.fork()
        if pid == 0:
            break
