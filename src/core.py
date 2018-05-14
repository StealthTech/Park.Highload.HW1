import fcntl
import os
import socket
import select

from http.generic import MimeTypeManager, ALLOWED_METHODS
from http.requests import HttpRequest
from http.responses.generic import HttpResponseOk, HttpResponseBadRequest, \
    HttpResponseForbidden, HttpResponseNotFound, HttpResponseMethodNotAllowed
from utils import get_socket, cpu_scale_fork, print_prefix

mt_manager = MimeTypeManager()


def process_request(request, document_root=''):
    mode = 'default'
    if request is None:
        return HttpResponseBadRequest(), None

    url = request.url

    if request.method not in ALLOWED_METHODS:
        return HttpResponseMethodNotAllowed(request.protocol), None

    if '../' in url:
        return HttpResponseForbidden(request.protocol), None

    if url[-1] == '/':
        mode = 'directory'
        url += 'index.html'

    filepath = os.path.join(document_root, url[1:])
    try:
        file = os.open(filepath, os.O_RDONLY)
        flag = fcntl.fcntl(file, fcntl.F_GETFL)
        fcntl.fcntl(file, fcntl.F_SETFL, flag | os.O_NONBLOCK)
    except IsADirectoryError:
        return HttpResponseForbidden(request.protocol), None
    except OSError:
        if mode == 'directory':
            return HttpResponseForbidden(request.protocol), None
        return HttpResponseNotFound(request.protocol), None

    _, extension = os.path.splitext(filepath)
    content_type = mt_manager.resolve(extension)
    content_length = os.path.getsize(filepath)

    if request.method == 'HEAD':
        file = None

    return HttpResponseOk(request.protocol, content_type, content_length), file


def process_epoll_in(epoll, fileno, connections, requests, responses, options):
    endl_1 = b'\n\n'
    endl_2 = b'\n\r\n'

    try:
        while True:
            buffer = connections[fileno].recv(1024)
            if not buffer:
                break
            requests[fileno] += buffer
    except socket.error:
        pass

    if endl_1 in requests[fileno] or endl_2 in requests[fileno]:
        epoll.modify(fileno, select.EPOLLOUT | select.EPOLLET)

    request_str = requests[fileno].decode()
    request = HttpRequest.from_string(request_str)

    resp, file = process_request(request, options['document_root'])

    buff = b""
    file_content = b""

    if file:
        while True:
            file_content += buff
            buff = os.read(file, 1024)
            if not buff:
                break
        os.close(file)

    responses[fileno] = resp.as_bytes() + file_content


def process_epoll_out(epoll, fileno, connections, requests, responses, options):
    try:
        while len(responses[fileno]) > 0:
            byteswritten = connections[fileno].send(responses[fileno])
            responses[fileno] = responses[fileno][byteswritten:]
    except socket.error:
        pass

    if len(responses[fileno]) == 0:
        epoll.modify(fileno, select.EPOLLET)
        connections[fileno].shutdown(socket.SHUT_RDWR)


def process_events(epoll, sock, options):
    connections = {}
    requests = {}
    responses = {}

    while True:
        events = epoll.poll(1)

        for fileno, event in events:
            if fileno == sock.fileno():
                try:
                    while True:
                        connection, address = sock.accept()
                        connection.setblocking(0)
                        epoll.register(connection.fileno(), select.EPOLLIN | select.EPOLLET)
                        connections[connection.fileno()] = connection
                        requests[connection.fileno()] = b''
                except socket.error:
                    pass

            elif event & select.EPOLLIN:  # Доступен для чтения
                process_epoll_in(epoll, fileno, connections, requests, responses, options)

            elif event & select.EPOLLOUT:  # Доступен для записи
                process_epoll_out(epoll, fileno, connections, requests, responses, options)

            elif event & select.EPOLLHUP:  # Отключение
                epoll.unregister(fileno)
                connections[fileno].close()
                del connections[fileno]


def start_polling(sock, options):
    epoll = select.epoll()
    epoll.register(sock.fileno(), select.EPOLLIN | select.EPOLLET)

    process_events(epoll, sock, options)

    epoll.unregister(sock.fileno())
    epoll.close()
    sock.close()
    print_prefix('EPoll instance closed.')


def start_server(options):
    print_prefix('Server is starting on {}:{}.'.format(options['ip_addr'], options['port']))
    print_prefix('Document root: {}.'.format(options['document_root']))
    print_prefix('CPU limit: {}'.format(options['cpu_limit']))

    sock = get_socket(options['ip_addr'], options['port'])

    cpu_scale_fork(options['cpu_limit'])

    start_polling(sock, options)
