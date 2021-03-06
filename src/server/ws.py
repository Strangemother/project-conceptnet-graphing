# import websocket
# ws = websocket.WebSocket()
# ws.connect("ws://example.com/websocket", http_proxy_host="proxy_host_name", http_proxy_port=3128)

from pocketsocket.ws import Client
from pocketsocket.client import ClientListMixin
from pocketsocket.server import Server


def main_echo():
    server = EchoServer()
    server.start()


class EchoClient(Client):
    def recv(self, data, opcode):
        # log('>', self, opcode, data)
        self.send_all(data, opcode, ignore=[self])

    def send(self, data, opcode=None):
        # log('<', self, opcode, data)
        return self.sendMessage(data, opcode)

class EchoServer(ClientListMixin, Server):
    ''' Basic instance of a server, instansiating ws.Client for
    socket clients '''
    ports = (9004, 9005, )
    address = '0.0.0.0'
    client_class = EchoClient


if __name__ == '__main__':
    main_echo()
