import socketserver
import threading
import config
from controller import controller
from user import User, PersonUser


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
    def handle(self):
        ip = self.client_address[0]
        print('TCP Connection:', ip)
        user = PersonUser.get(ip, ip)
        print(user)
        print(User.users)

        while True:
            data = self.request.recv(64)
            if not data:
                break
            print('Data:', repr(data), list(data))
            controller.send_command(data, user=user.name)
            #print('Sent to origin')
        #self.request.sendall(data, self.client_address)


class UDPHandler(Handler):
    def handle(self):
        data, sock = self.request
        if data == b'MAX-REMOTE':
            print('Handshake:', self.client_address[0])
        else:
            print('UDP Data:', repr(data))

        sock.sendto(config.server_name, self.client_address)


def load(daemon=True):
    host = config.parser.gete('server', 'addr')
    port = config.parser.gete('server', 'port')

    server_tcp = TCPServer((host, port), Handler)
    server_udp = UDPServer((host, port), UDPHandler)
    print(host, ':', port, sep='')

    threading.Thread(target=server_tcp.serve_forever, daemon=daemon).start()
    threading.Thread(target=server_udp.serve_forever, daemon=daemon).start()


if __name__ == '__main__':
    load(False)
