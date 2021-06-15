import socket
import logging
from configparser import ConfigParser
from response import Response


class ClientDisconnected(Exception):

    def __init__(self):
        pass


class NetworkManager:
    """
    Manages the communication between sc-driver and sc-master sending and receiving messages specified in a simple
    protocol called SCP over TCP. Messages (BOTH requests and responses) are defined as UTF-8 encoded strings containing
    the JSON representation of the commands for instance:

    - {"name": "set_color"  ->  bad
    - {"name": "set_color"} ->  ok

    Messages MUST be finalized with a special string defined con config.ini

    """

    # TODO: test sending multiple commands in a short period of time

    def __init__(self, config: ConfigParser):
        self.host = config['DEFAULT'].get('host', '0.0.0.0')
        self.port = int(config['DEFAULT'].get('port', str(8000)))
        self.tcp_max_queue = int(config['DEFAULT'].get('tcp_max_queue', str(10)))
        self.tcp_max_msg_size = int(config['DEFAULT'].get('tcp_max_msg_size', str(1024)))
        self.tcp_msg_encoding = config['DEFAULT'].get('tcp_msg_encoding', 'UTF-8')
        self.logger = logging.getLogger()
        self.skt_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.skt_client = None
        self.end_char = '\n'

    def start(self):
        """
        Socket binding and listening
        """
        self.skt_server.bind((self.host, self.port))
        self.skt_server.listen(self.tcp_max_queue)
        self.logger.info(f'Listening on {self.host}:{self.port}')

    def stop(self):
        """
        Closes server and client sockets
        """
        if self.skt_client is not None:
            self.skt_client.close()
            self.logger.info('Client socket closed.')
        self.skt_server.close()
        self.logger.info('Server socket closed.')

    def accept_client(self):
        """
        Accepts connection for ONLY ONE client
        """
        self.skt_client, address = self.skt_server.accept()
        self.logger.info(f'New client connected from {address[0]}:{address[1]}')

    def disconnect_client(self):
        """
        Closes client socket
        """
        if self.skt_client is not None:
            self.skt_client.close()
            self.logger.info('Client socket closed')

    def receive(self) -> str:
        """
        Receives a command from the client.

        :return: stringified JSON representation of the command
        :raises ClientDisconnected: if client disconnect from sc-driver
        """
        logger = logging.getLogger()

        # Receiving headers
        msg = ''
        end = self.end_char.encode(self.tcp_msg_encoding)
        chunk = self.skt_client.recv(1)
        while len(chunk) > 0 and chunk != end:
            msg += chunk.decode(self.tcp_msg_encoding)
            chunk = self.skt_client.recv(1)
        if len(chunk) == 0:
            logger.warning('Client disconnected abruptly')
            raise ClientDisconnected()
        else:
            msg += chunk.decode(self.tcp_msg_encoding)
            logger.info('Command received')
            return msg

    def send(self, response: Response):
        """
        Sends a message to the client.
        """
        msg = (response.to_json() + self.end_char).encode(self.tcp_msg_encoding)
        sent = self.skt_client.send(msg)
        msg = msg[sent:]
        while len(msg) > 0:
            sent = self.skt_client.send(msg)
            msg = msg[sent:]
