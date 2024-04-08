
import socket
import threading
import numpy as np


class audioServer:
    def __init__(self):
        self.ip = socket.gethostbyname(socket.gethostname())
        print(self.ip)
        while True:
            try:
                self.port = 9808
                self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.s.bind((self.ip, self.port))
                break
            except:
                print("Couldn't bind to that port")

        #self.audio_buffer = []
        self.connections = []
        # self.stream = sd.OutputStream(callback=self.audio_callback)
        # self.stream.start()
        self.running = True  # add this line
        self.accept_connections()

    def accept_connections(self):
        self.s.listen(100)

        print("Running on IP: " + self.ip)
        print("Running on port: " + str(self.port))

        while self.running:
            c, addr = self.s.accept()
            self.connections.append(c)
            threading.Thread(
                target=self.handle_client,
                args=(
                    c,
                    addr,
                ),
            ).start()

    def broadcast(self, sock, data):
        for client in self.connections:
            if client != self.s and client != sock:
                try:
                    client.send(data)
                except:
                    pass

    def handle_client(self, c, addr):
        while 1:
            try:
                data = c.recv(1024)
                # print(data)
                # self.audio_buffer.append(data)
                self.broadcast(c, data)

            except socket.error:
                c.close()

    def close(self):
        self.running = False
        for c in self.connections:
            c.close()
        self.s.close()


server = audioServer()


