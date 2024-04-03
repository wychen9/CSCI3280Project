from Room import Room
from Member import Member, memberList
import socket
import threading
ip = '127.0.0.1'
port = 8888
MAX_USER = 10
class Room_Server():
    def __init__(self):
        # roomList - save rooms on the server in list [Room objects]
        self.roomList = []
        self.memberList = memberList
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.s.bind((ip, port))
        self.s.listen(1)
        self.roomListLock = threading.Lock()
        
        multhd = []
        for i in range(MAX_USER):
            multhd.append(threading.Thread(target=self.connect_with_client))
        for i in multhd:
            i.setDaemon(1)
            i.start()
        for i in multhd:
            i.join()

    def connect_with_client(self):
        while True:
            try: 
                sock,addr = self.s.accept()
                print("Connection from addr: ", addr)
                sock.send(b"Connected to the server.")
                self.recv_from_client(sock, addr)
            except Exception as e:
                print('Exception when connecting with client: ' + str(e))

    def recv_from_client(self, sock, addr):
        flag = True
        # receive request from client
        while flag:
            msg = sock.recv(1024).decode('UTF-8')
            if(msg!=''): print(str(addr) + ': '+  msg)

            reqs = msg.split('@')
            for string in reqs:
                req = string.split('#')
                if(req[0] == 'c'):
                    self.create_room(req[1], req[2], sock)
                elif req[0] == 'j':
                    self.join_room(req[1], req[2], sock)
                elif req[0] == 'l':
                    self.leave_room(req[1], req[2], sock)
                elif req[0] == 'r':
                    self.get_room_list(sock)
                elif req[0] == 'n':
                    self.get_room_count(req[1], sock)
                elif req[0] == 'e':
                    self.log_out(sock)
                    flag = False
                    break
        print(str(addr) + ' ended the client program.')
                

    def create_room(self, name, mem, sock):
        # name - (String) room name
        # mem - (String) member id
        # sock - socket channel
        #
        # create a new room with given name and add the member to the room
        # if the name is already existed, nothing will be done.
        # no return
        if(name in [r.roomName for r in self.roomList]):
            # self.join_room(name, mem, sock)
            msg = 'Room ' + name + ' has already existed.'+ '@'
            sock.send(str.encode(msg))
        else:
            self.roomListLock.acquire()
            new_room = Room(name)
            new_room.joinMember(self.memberList[int(mem)])
            self.roomList.append(new_room)
            self.roomListLock.release()

            msg = 'New room ' + name + ' created.'+ '@'
            sock.send(str.encode(msg))
        
            

    def get_room_list(self, sock):
        # return - return current room list
        roomNames = [r.roomName for r in self.roomList]
        msg = '%'.join(roomNames) + '&@'
        print("Current Room List: ")
        print([r.roomName for r in self.roomList])
        print('members in rooms: ')
        print([[m.name for m in r.members] for r in self.roomList])
        sock.send(str.encode(msg))

    def get_room_count(self, roomName, sock):
        # return - return number of current members in the given room
        if(roomName in [r.roomName for r in self.roomList]): 
            room = list(filter(lambda r: r.roomName == roomName,self.roomList))[0]
            msg = str(room.current_cnt())
            sock.send(str.encode(msg))
        else: 
            msg = "No such room found."
            print(msg)
            sock.send(str.encode(msg))

    def join_room(self, roomName, mem, sock):
        # roomName - room name
        # mem - member id
        # sock - socket channel
        #
        # The user will be added to according room.
        # If the user has already been in the room, no action will be taken.
        # No return.
        if(roomName in [r.roomName for r in self.roomList]): 
            room = list(filter(lambda r: r.roomName == roomName,self.roomList))[0]
            member = memberList[int(mem)]
            if(member in room.members):
                msg = member.name + ' has already been in Room ' + roomName + '.'+ '@'
                sock.send(str.encode(msg))
            else:
                self.roomListLock.acquire()
                room.joinMember(member)
                self.roomListLock.release()
                msg = member.name + ' has joined Room ' + roomName + '.'+ '@'
                sock.send(str.encode(msg))
        else: 
            msg = "No such room found."
            print(msg)
            sock.send(str.encode(msg))

    def leave_room(self, roomName, mem, sock):
        # roomName - room name
        # mem - member id
        # sock - socket channel
        #
        # The user will be removed from according room.
        # If the user has not been in the room, no action will be taken.
        # No return.
        if(roomName in [r.roomName for r in self.roomList]): 
            room = list(filter(lambda r: r.roomName == roomName,self.roomList))[0]
            member = self.memberList[int(mem)]
            if(member in room.members):
                self.roomListLock.acquire()
                room.leaveMember(member)
                self.roomListLock.release()
                msg = member.name + ' has left Room ' + roomName + '.'+ '@'
                sock.send(str.encode(msg))
                if(room.isEmpty()): 
                    self.roomList.remove(room)
            else: 
                msg = member.name + ' has not been in Room ' + roomName + ' yet.'+ '@'
                sock.send(str.encode(msg))
        else: 
            msg = "No such room found."
            print(msg)
            sock.send(str.encode(msg))

    def log_out(self, sock):
        # end the connection session
        msg = 'Connection is closed from client side.@'
        sock.send(str.encode(msg))
        sock.close()

srv = Room_Server()
