from Room import Room
from Member import Member, memberList
import socket
import threading
ip = '127.0.0.1'
port = 8888
NUM_OF_THREADS = 5
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
        for i in range(NUM_OF_THREADS):
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
                elif req[0] == 'e':
                    self.log_out(sock)
                    flag = False
                    break
        print(str(addr) + ' ended the client program.')
                

    def create_room(self, name, mem, sock):
        # Develop a function that allows users to create a new chat room.
        # This function should enable other computers on the same network to discover and access the created chat room
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
        # Implement a 'chat room list' feature that displays all the created chat rooms within the network. 
        # This list will help users identify and select the chat room they wish to join
        # return - return the room name when find a room
        roomNames = [r.roomName for r in self.roomList]
        msg = '%'.join(roomNames) + '&@'
        print("Current Room List: ")
        print([r.roomName for r in self.roomList])
        print('members in rooms: ')
        print([[m.name for m in r.members] for r in self.roomList])
        sock.send(str.encode(msg))

    def join_room(self, roomName, mem, sock):
        # Create a function that enables users to join a selected chat room from the 'chat room list'. 
        # This functionality should establish a connection with the chosen chat room, allowing users to participate in real-time communication.
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
        msg = 'Connection is closed from client side.@'
        sock.send(str.encode(msg))
        sock.close()

srv = Room_Server()
