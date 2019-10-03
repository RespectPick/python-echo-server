import yaml
import json
import zlib
import socket
import threading
from datetime import datetime
from argparse import ArgumentParser


def make_request(action, text, date=datetime.now()):
    return {
        'action': action,
        'data': text,
        'time': date.timestamp()
    }


def read(sock, buffersize):
    while True:
        compressed_response = sock.recv(buffersize)
        bytes_response = zlib.decompress(compressed_response)
        response = json.loads(bytes_response)
        print(response)

if __name__ == '__main__':
    config = {
        'host': 'localhost',
        'port': 8500,
        'buffersize': 1024
    }

    parser = ArgumentParser()
    parser.add_argument('-c', '--config', type=str, required=False, help='config file')
    parser.add_argument('-ht', '--host', type=str, required=False, help='server host')
    parser.add_argument('-p', '--port', type=str, required=False, help='server port')

    args = parser.parse_args()

    if args.config:
        with open(args.config) as file:
            file_config = yaml.safe_load(file)
            config.update(file_config or {})

    host = args.host if args.host else config.get('host')
    port = args.port if args.port else config.get('port')
    buffersize = config.get('buffersize')

    try:
        sock = socket.socket()
        sock.connect((host, port))

        read_thread = threading.Thread(target=read, args=(sock, buffersize))
        read_thread.start()

        while True:
            action = input('Enter action name: ')
            message = input('Enter your message: ')

            request = make_request(action, message)
            str_request = json.dumps(request)
            bytes_request = str_request.encode()
            compressed_request = zlib.compress(bytes_request)
            sock.send(compressed_request)

    except KeyboardInterrupt:
        print('Client shoutdown')
