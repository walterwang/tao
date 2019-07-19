import socket
import threading
import socketserver
import time
from matchmaking import Matcher
from queue import Queue
from handler import Handler


class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    def __init__(self, request, client_address, server):
        self.game = server.game
        self.notify_q = server.notify_q
        socketserver.BaseRequestHandler.__init__(self, request, client_address, server)

    def handle(self):
        handle = Handler(self)
        handle()


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    def __init__(self, server_address, RequestHandlerClass,
                 bind_and_activate=True, queue=None):
        self.game = queue[0]
        self.notify_q = queue[1]
        socketserver.TCPServer.__init__(self, server_address, RequestHandlerClass,
                           bind_and_activate=bind_and_activate)


if __name__ == '__main__':
    game = {}
    notify_q = Queue()
    HOST, PORT = 'localhost', 9999

    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler,
                               queue=[game, notify_q])

    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    Matcher(game).start() 
    
    print("server loop running in thread:", server_thread.name)

    time.sleep(20)
    server.shutdown()
