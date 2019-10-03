import yaml
import socket
import logging
import select
import threading
from argparse import ArgumentParser

from hanlers import handle_tcp_request
from resolvers import find_server_actions


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

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=(
        logging.FileHandler('server.log'),
        logging.StreamHandler()
    )
)

requests = []
connections = []


def read(sock, requests, buffersize):
    bytes_request = sock.recv(buffersize)

    if bytes_request:
        requests.append(bytes_request)


def write(sock, response):
    sock.send(response)


try:
    sock = socket.socket()
    sock.bind((host, port))
    sock.setblocking(0)
    sock.listen(5)

    logging.info(f'Server started {host} : {port}')
    action_mapping = find_server_actions()

    while True:
        try:
            client, (client_host, client_port) = sock.accept()
            logging.info(f'Client {client_host}:{client_port}')
            connections.append(client)
        except:
            pass

        rlist, wlist, exlist = select.select(
            connections, connections, connections, 0
        )

        for read_client in rlist:
            read_thread = threading.Thread(target=read, args=(read_client, requests, buffersize))
            read_thread.start()

        if requests:
            bytes_request = requests.pop()
            bytes_response = handle_tcp_request(bytes_request, action_mapping)

            for write_client in wlist:
                write_thread = threading.Thread(target=write, args=(write_client, bytes_request))
                write_thread.start()

except KeyboardInterrupt:
    logging.info('server shutdown')
