import socket
import threading
import socketserver
import time

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        while True:
            data = str(self.request.recv(1024))
            cur_thread = threading.current_thread()
            response = '{}: {}'.format(cur_thread.name, data.upper())
            self.request.sendall(response.encode())

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

if __name__ == '__main__':
    HOST, PORT = 'localhost', 9999

    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)

    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()

    print("server loop running in thread:", server_thread.name)

    time.sleep(100)
    server.shutdown()
