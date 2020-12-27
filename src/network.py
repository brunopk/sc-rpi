import socket
import logging
import re

from configparser import ConfigParser


class SCPError(Exception):

    def __init__(self, msg: str):
        self.msg = msg

    def get_msg(self) -> str:
        return self.msg


class Message:

    def __init__(self, body: str, encoding: str):
        self.body = body
        self.encoding = encoding

    def get_body(self) -> str:
        return self.body

    def __bytes__(self):
        separator = '\r\n'
        content_length_header = f'Content-Length: {len(self.body)}'
        msg = content_length_header + separator + separator + self.body
        return msg.encode(self.encoding)


class NetworkManager:
    """
    Manages the communication between sc-driver and sc-master sending and receiving messages specified in a protocol
    called SCP specifically designed for this system. It works through TCP and it's similar to HTTP. Messages
    (BOTH requests and responses) are defined as UTF-8 encoded strings with two sections :

        - Headers
        - Body

    Headers:

        Headers MUST contain the following pattern:

            Content-Length: <INTEGER><CARRIAGE_RETURN><END_OF_LINE>

        respecting this simple rules :

            - It's all case-sensitive
            - <INTEGER> represents the command length in bytes with NO MORE than 7 digits.
            - Between 'Content-Length:' and <INTEGER> there's a space

    Body:

        Contains the JSON representation of the command, for instance:

            - {"name": "set_color"  ->  bad
            - {"name": "set_color"} ->  ok

        Take into account that <CARRIAGE_RETURN><END_OF_LINE> in the body will count as 2 bytes of the total
        body size defined in headers.

    """

    def __init__(self, config: ConfigParser):
        self.host = config['DEFAULT'].get('host', '0.0.0.0')
        self.port = int(config['DEFAULT'].get('port', str(8000)))
        self.tcp_max_queue = int(config['DEFAULT'].get('tcp_max_queue', str(10)))
        self.tcp_max_msg_size = int(config['DEFAULT'].get('tcp_max_msg_size', str(1024)))
        self.tcp_msg_encoding = config['DEFAULT'].get('tcp_msg_encoding', 'UTF-8')
        self.logger = logging.getLogger('NetworkManager')
        self.skt_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.skt_client = None

    def start(self):
        """
        Socket binding and listening
        """
        self.skt_server.bind((self.host, self.port))
        self.skt_server.listen(self.tcp_max_queue)
        self.logger.info(f'Listening on {self.host}:{self.port}')

    def accept(self):
        """
        Accepts connection for ONLY ONE client
        """
        self.skt_client, address = self.skt_server.accept()
        self.logger.info(f'New client connected from {address[0]}:{address[1]}')

    def close(self):
        """
        Close server socket
        """
        self.skt_server.close()
        self.logger.info('Socket closed')

    def receive(self) -> Message:
        """
        Receives a message from the client.

        :raises NetworkError: in case of not respecting any of the mentioned rules
        """
        logger = logging.getLogger()

        # Receiving headers
        msg = ''
        chunk = self.skt_client.recv(2)
        while '\r\n' not in msg:
            msg += str(chunk.decode(self.tcp_msg_encoding))
            chunk = self.skt_client.recv(2)
        msg += str(chunk.decode(self.tcp_msg_encoding))
        regex = r"^Content-Length:\s(\d{1,7})"
        match = re.match(regex, msg)
        if match is not None:
            groups = match.groups()
            body_size = int(groups[0])
        else:
            logger.warning('invalid message received')
            raise SCPError('Content-Length not defined correctly')
        #regex = r"^Content-Length:\s(\d{1,7})\r\n\r\n[^\r\n]"
        #match = re.match(regex, msg)
        #if match is None:
        #    logger.warning('invalid message received')
        #    raise SCPError('header section must end with only one \r\n')

        # Receiving body
        body = ''
        max_headers_size = 27
        chunk = self.skt_client.recv(body_size)
        while len(body) < body_size:
            msg += str(chunk.decode(self.tcp_msg_encoding))
            regex = r"^Content-Length:\s\d{1,7}\r\n\r\n(.+)"
            match = re.match(regex, msg, flags=re.MULTILINE)
            body = match.groups()[0]
            if len(body) < body_size:
                chunk = self.skt_client.recv(body_size)
            if len(msg) > max_headers_size + body_size:
                raise SCPError('message is longer than specified size')

        logger.info('Message received')
        return Message(body, self.tcp_msg_encoding)

    def send(self, msg: str):
        """
        Sends a message to the client.
        """
        msg = bytes(Message(msg, self.tcp_msg_encoding))
        remaining = self.skt_client.send(msg)
        while remaining > 0:
            remaining = self.skt_client.send(msg[remaining:])
