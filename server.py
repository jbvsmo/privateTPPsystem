import socketserver
import threading
import config
import buffer
import controller
from user import PersonUser
from log import logger


class OriginServer(object):
    pass


class TCPServer(
    socketserver.ThreadingMixIn,
    socketserver.TCPServer
):
    pass


class UDPServer(
    socketserver.ThreadingMixIn,
    socketserver.UDPServer
):
    pass


class Handler(socketserver.BaseRequestHandler):
    user = None
    buffer = None

    def handle(self):
        self.buffer = buffer.Buffer(self.request)
        ip = self.client_address[0]
        self.user = PersonUser.get(ip, ip)
        #print('TCP Connection:', self.user)
        logger.debug(type='tcp', action='connection',
                     user=[self.user.ip, self.user.name],
                     content=None)

        while True:
            try:
                content = self.read_command()
            except buffer.SocketClosedError:
                return
            self.handle_content(content)

    def read_command(self):
        startbyte = None
        while startbyte != controller.command_header:
            startbyte = self.buffer.read(1, True)

        size = self.buffer.read(1, True)
        return self.buffer.read(size[0], True)

    def handle_content(self, content):
        orig_content = content
        content = controller.find_command(content)
        if content is None:
            logger.debug(type='tcp', action='invalid_command',
                         user=[self.user.ip, self.user.name],
                         content=orig_content)
            return

        logger.debug(type='tcp', action='command',
                     user=[self.user.ip, self.user.name],
                     content=content, bytes=orig_content)

        cmd, st = content
        if st == controller.CommandType.text:
            self.user.name = cmd  # TODO change user name on interface too?
            return

        controller.controller_instance.send_command(content, user=self.user.name)


class UDPHandler(Handler):
    def handle(self):
        data, sock = self.request
        if data == b'MAX-REMOTE':
            logger.log(type='udp', action='handshake',
                       content=self.client_address)
        else:
            logger.log(type='udp', action='data',
                       content=repr(data))

        sock.sendto(config.server_name, self.client_address)


def load(daemon=True):
    host = config.parser.gete('server', 'addr')
    port = config.parser.gete('server', 'port')

    server_tcp = TCPServer((host, port), Handler)
    server_udp = UDPServer((host, port), UDPHandler)
    #print(host, ':', port, sep='')
    logger.info(type='meta', action='server_listen',
                content='{}:{}'.format(host, port))

    threading.Thread(target=server_tcp.serve_forever, daemon=daemon).start()
    threading.Thread(target=server_udp.serve_forever, daemon=daemon).start()


if __name__ == '__main__':
    load(False)
