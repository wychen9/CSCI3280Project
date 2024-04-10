import socket
import threading
#import opuslib


class audioServer:
    def __init__(self):
        self.ip = socket.gethostbyname(socket.gethostname())
        #self.ip = "10.13.79.153"
        #print(self.ip)
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

        # self.encoder = opuslib.Encoder(48000, 2, opuslib.APPLICATION_AUDIO)
        # self.decoder = opuslib.Decoder(48000, 2)

        self.accept_connections()

    def accept_connections(self):
        self.s.listen(100)

        print("Running on IP: " + self.ip)
        print("Running on port: " + str(self.port))

        while self.running:
            c, addr = self.s.accept()
            self.connections.append(c)
            print(f'Client {addr} connected')
            threading.Thread(
                target=self.handle_client,
                args=(
                    c,
                    addr,
                ),
            ).start()

    def broadcast(self, room, sock, data):
        #opus_data = self.encoder.encode(data, 960)
        for client in self.rooms[room]:
            if client != sock:
                try:
                    client.send(data)
                    #print(f"Broadcasted data to client {client.getpeername()} in room {room}")
                except:
                    pass

    def handle_client(self, c, addr):
        room = None
        while 1:
            try:
                data = c.recv(1024)
                #print(data.decode())
                if data.startswith(b"join"):
                    room = data.split(b" ")[1].decode()
                    if room not in self.rooms:
                        self.rooms[room] = []
                        print(f'Room {room} created')
                    self.rooms[room].append(c)
                    print(f"Client {addr} has joined room {room}")
                elif data.startswith(b"leave"):
                    room = data.split(b" ")[1].decode()
                    self.rooms[room].remove(c)
                    print(f'Client {addr} has left room {room}')
                    if not self.rooms[room]:
                        del self.rooms[room]
                        print(f'Room {room} deleted')
                        room = None
                else:
                    if room is not None:
                        #pcm_data = self.decoder.decode(data, 960)
                        self.broadcast(room, c, data)

            except socket.error:
                c.close()
                # if room is not None and c in self.rooms[room]:
                #     self.rooms[room].remove(c)
                print(f'Client {addr} disconnected')
                break

            # finally:
            #     c.close()
            #     if room is not None:
            #         self.rooms[room].remove(c)
            #     print(f'Client {addr} disconnected')

    def close(self):
        self.running = False
        for c in self.connections:
            c.close()
        self.s.close()
        print('Server stopped')


server = audioServer()

