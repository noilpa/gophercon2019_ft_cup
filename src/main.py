import socket
import json
from pyreindexer import RxConnector
import time
import macpath


URLS = {
    '/': 'hello index',
    '/api/v1/search': 'hello search'
}


def elapse_time(f):
    def wrapper(*args, **kwargs):
        t = time.time()
        res = f(*args, **kwargs)
        print((time.time() - t), 's')
        return res
    return wrapper


def generate_headers(method, url):
    if method != 'GET':
        return 'HTTP/1.1 405 Method not allowed\n\n', 405
    if url not in URLS.keys():
        return 'HTTP/1.1 404 Not found\n\n', 404
    return 'HTTP/1.1 200 OK\n\n', 200


def parse_request(request):
    parsed = request.split(' ')
    method, url = parsed[0], parsed[1]
    return method, url


def generate_response(request):
    method, url = parse_request(request)
    headers, code = generate_headers(method, url)
    body = ''
    if code == 200:
        body = URLS[url]

    return (headers + body).encode()


def run():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', 9080))
    server_socket.listen()

    while True:
        client_socket, addr = server_socket.accept()
        request = client_socket.recv(1024)
        response = generate_response(request.decode('utf-8'))
        client_socket.send(response)
        client_socket.close()


def save_to_rx(db: RxConnector, namespace: str):
    pass


@elapse_time
def read_json(paths: list):
    for path in paths:
        with open(path) as f:
            data = json.load(f)
            print(data)
            print('\n\n\n\n')


if __name__ == '__main__':
    paths = [
        '../data/ammos.json',
        '../data/epg.json',
        '../data/media_items.json',
    ]
    read_json(paths)



