from Room import Room
import socket
#  CHAT ROOM NAME CANNOT CONTAIN '&', '%', '#' and '@' !!!
ip = '127.0.0.1'
port = 8888

class Room_Client():
    def __init__(self, mem):
        # mem - (Member)member logged in
        # initialize the client program to connect to the server
        # No return
        #
        # commands to server
        # c - create a new room
        # j - join a room
        # l - leave a room
        # r - retrieve room list
        # e - end connection with the server
        self.mem = mem
        self.roomList = []

        # connect to server
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.s.connect((ip,port))
        self.recv_from_srv()

    def create_room(self, name):
        # name - (String) room name
        # send the name of the room you want to create
        msg = 'c#' + name + '#' + self.mem.id + '@'
        self.s.send(str.encode(msg))
        self.recv_from_srv()
    
    def get_room_list(self):
        # get current room list
        # return - (List) current room list
        msg = 'r@'
        self.s.send(str.encode(msg))
        res = self.recv_from_srv()
        for content in res:
            if '&' in content:
                content = content.replace('&','')
                self.roomList = content.split('%')
        print('roomList in Client: ' + str(self.roomList))
        return self.roomList

    def join_room(self, roomName):
        # roomName - (String) room name
        # send the name of the room you want to join
        msg = 'j#'+roomName+'#'+ self.mem.id+ '@'
        self.s.send(str.encode(msg))
        self.recv_from_srv()

    def leave_room(self, roomName):
        # roomName - (String) room name
        # send the name of the room you want to leave
        msg = 'l#'+roomName+'#'+ self.mem.id+ '@'
        self.s.send(str.encode(msg))
        self.recv_from_srv()
    
    def exit(self):
        # exit the program and close the connection with the server
        msg = 'e@'
        self.s.send(str.encode(msg))
        self.recv_from_srv()
        self.s.close()

    def recv_from_srv(self):
        buffer = []
        d = self.s.recv(1024)
        buffer.append(d)
        data = b''.join(buffer)
        msgs = str(data,'UTF-8').split('@')
        msgs = list(filter(lambda x: x!= '', msgs))
        for msg in msgs:
            if(not '%' in msg): print(self.mem.name + ': '+  msg)
        return msgs