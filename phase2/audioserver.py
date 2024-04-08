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

        self.rooms = {} 
        self.connections = []
        self.running = True
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

    def broadcast(self, room, sock, data):
        for client in self.rooms[room]:
            if client != sock:
                try:
                    client.send(data)
                except:
                    pass

    def handle_client(self, c, addr):
        room = None
        while 1:
            try:
                data = c.recv(1024)
                if data.startswith("join:"):
                    room = data.split(":")[1]
                    if room not in self.rooms:
                        self.rooms[room] = []
                    self.rooms[room].append(c)
                elif data.startswith("leave:"):
                    room = data.split(":")[1]
                    self.rooms[room].remove(c)
                    room = None
                else:
                    if room is not None:
                        self.broadcast(room, c, data)

            except socket.error:
                c.close()
                if room is not None:
                    self.rooms[room].remove(c)

    def close(self):
        self.running = False
        for c in self.connections:
            c.close()
        self.s.close()


server = audioServer()

