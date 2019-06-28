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


#        while True:
#            data = str(self.request.recv(1024))
#            print(data) 
#            #item = self.queue.get()
#            cur_thread = threading.current_thread()
#            if data == "b'ready'":
#                response = '{}: ready recieved'.format(cur_thread.name)
#                self.request.sendall(response.encode())
#
#                self.mm_q.put(f"{cur_thread.name} is ready")
#            if data == "b'check'":
#                q = self.mm_q.get()
#                response = '{}:whats in queue: {}'.format(cur_thread.name, q)
#                self.request.sendall(response.encode())
#            if data == "b'start'":
#                send_q = Queue()
#                send_q.put('{} in the send q'.format(cur_thread))
#                self.notify_q.put(send_q)
#                self.request.sendall('start received, send_q created and putinto notify_q'.encode())
#            if data == "b'notified'":
#                s = self.notify_q.get()
#                response = s.get()
#                self.request.sendall(response.encode())

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
    
    print("server loop running in thread:", server_thread.name)

    time.sleep(20)
    server.shutdown()
