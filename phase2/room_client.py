from Room import Room
from Member import Member, memberList
import socket
import threading
import time
#  CHAT ROOM NAME CANNOT CONTAIN '%', '#' and '@'
ip = '127.0.0.1'
port = 8888


class Room_Client():
    def __init__(self, mem):
        # mem - (Member)member logged in
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
        
        # get connection results from server
        self.recv_from_srv()

    def create_room(self, name):
        msg = 'c#' + name + '#' + self.mem.id + '@'
        self.s.send(str.encode(msg))
        self.recv_from_srv()
    
    def get_room_list(self):
        msg = 'r@'
        self.s.send(str.encode(msg))
        res = self.recv_from_srv()
        for content in res:
            if '%' in content:
                self.roomList = content.split('%')
        print('roomList in Client: ' + str(self.roomList))

    def join_room(self, roomName):

        msg = 'j#'+roomName+'#'+ self.mem.id+ '@'
        self.s.send(str.encode(msg))
        self.recv_from_srv()

    def leave_room(self, roomName):
        msg = 'l#'+roomName+'#'+ self.mem.id+ '@'
        self.s.send(str.encode(msg))
        self.recv_from_srv()
    
    def end_connect(self):
        msg = 'e@'
        self.s.send(str.encode(msg))
        self.s.close

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
    
    def wait_until(self, ret, init_val, timeout, period=0.25):
        mustend = time.time() + timeout
        while time.time() < mustend:
            if ret != init_val: return True
            time.sleep(period)
        return False

m1 = memberList[1]
c1 = Room_Client(m1)
c1.create_room('My Chat Room')
c1.create_room('Chat Room 2')
c1.get_room_list()
c1.join_room('Special Room')
c1.get_room_list()
c1.end_connect()