from Room import Room
from Member import memberList
import sys, os
import socket
import threading
ip = '127.0.0.1'
port = 8888
MAX_USER = 10
class Room_Server():
    def __init__(self):
        # roomList - save rooms on the server in list [Room objects]
        #
        # labels sent to client:
        # @ - end of a msg
        # & - have return
        # # - splitter of return params
        # % - list splitter
        self.roomList = []
        self.memberSockList = [None]*10
        self.ip = socket.gethostbyname(socket.gethostname())
        print("Server IP: ", self.ip)
        print("Server port: ", port)
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.s.bind((self.ip, port))
        self.s.listen(1)
        self.roomListLock = threading.Lock()
        self.sockListLock = threading.Lock()
        
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
            sock,addr = self.s.accept()
            print("Connection from addr: ", addr)
            sock.send(b"Connected to the server.@")
            self.recv_from_client(sock, addr)

            # try: 
                
            # except Exception as e:
            #     exc_type, exc_obj, exc_tb = sys.exc_info()
            #     fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            #     print('Exception when connecting with client: ')
            #     print(exc_obj, fname, exc_tb.tb_lineno)

    def recv_from_client(self, sock, addr):
        flag = True
        # receive request from client
        while flag:
            msg = sock.recv(1024).decode('UTF-8')
            if(msg!=''): print(str(addr) + ': '+  msg)

            reqs = list(filter(lambda x: x!= '', msg.split('@')))
            # print(reqs)
            for string in reqs:
                req = string.split('#')
                if req[0].isnumeric():
                    ind = int(req[0])
                    self.sockListLock.acquire()
                    self.memberSockList[ind] = sock
                    self.sockListLock.release()
                else:
                    if req[0] == 'c':
                        self.create_room(req[1], int(req[2]))
                    elif req[0] == 'j':
                        self.join_room(req[1], int(req[2]))
                    elif req[0] == 'l':
                        self.leave_room(req[1], int(req[2]))
                    elif req[0] == 'r':
                        self.get_room_list(sock)
                    elif req[0] == 'n':
                        self.get_room_count(req[1], sock)
                    elif req[0] == 'm':
                        self.get_member_count(req[1], sock)
                    elif req[0] == 'e':
                        self.log_out(sock)
                        flag = False
                        break
        print(str(addr) + ' ended the client program.')
                

    def create_room(self, name, ind):
        # name - (String) room name
        # ind - (String) member id
        #
        # create a new room with given name and add the member to the room
        # if the name is already existed, nothing will be done.
        # Return updated memberlist to all client in corresponding room
        sock = self.memberSockList[ind]
        if(name in [r.roomName for r in self.roomList]):
            # self.join_room(name, mem, sock)
            msg = 'F&@'
        else:
            self.roomListLock.acquire()
            new_room = Room(name)
            new_room.joinMember(memberList[ind])
            self.roomList.append(new_room)
            self.roomListLock.release()
            self.inform_client('j', name, ind)
            msg = 'T&@'
        # print('msg for create: ' + msg)
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
            msg = str(room.current_cnt()) + '&@'
            sock.send(str.encode(msg))
        else: 
            msg = "No such room found.@"
            print(msg.replace('@',''))
            sock.send(str.encode(msg))

    def get_member_count(self, roomName, sock):
        # return - return number of current members in the given room
        if(roomName in [r.roomName for r in self.roomList]): 
            room = list(filter(lambda r: r.roomName == roomName,self.roomList))[0]
            memberList = [m.name for m in room.members]
            msg = '%'.join(memberList) + '&@'
            sock.send(str.encode(msg))
        else: 
            msg = "No such room found.@"
            print(msg.replace('@',''))
            sock.send(str.encode(msg))

    def join_room(self, roomName, ind):
        # roomName - room name
        # mem - member id
        # sock - socket channel
        #
        # The user will be added to according room.
        # If the user has already been in the room, no action will be taken.
        # Return updated memberlist to all client in corresponding room
        sock = self.memberSockList[ind]
        if(roomName in [r.roomName for r in self.roomList]): 
            room = list(filter(lambda r: r.roomName == roomName,self.roomList))[0]
            member = memberList[ind]
            if(member in room.members):
                msg = 'F&@'
                sock.send(str.encode(msg))
            else:
                self.roomListLock.acquire()
                room.joinMember(member)
                self.roomListLock.release()
                for member in room.members:
                    self.inform_client('j', roomName, int(member.id))
                msg = 'T&@'
                sock.send(str.encode(msg))
        else: 
            msg = 'F&@'
            sock.send(str.encode(msg))

    def leave_room(self, roomName, ind):
        # roomName - room name
        # mem - member id
        # sock - socket channel
        #
        # The user will be removed from according room.
        # If the user has not been in the room, no action will be taken.
        # Return updated memberlist to all client in corresponding room
        sock = self.memberSockList[ind]
        if(roomName in [r.roomName for r in self.roomList]): 
            room = list(filter(lambda r: r.roomName == roomName,self.roomList))[0]
            member = memberList[ind]
            if(member in room.members):
                self.roomListLock.acquire()
                room.leaveMember(member)
                self.roomListLock.release()
                
                for member in room.members:
                    self.inform_client('l', roomName, int(member.id))
                
                if(room.isEmpty()): 
                    self.roomList.remove(room)
                msg = 'You have left room ' + roomName + '.@'
                sock.send(str.encode(msg))
            else: 
                msg = member.name + ' has not been in Room ' + roomName + ' yet.@'
                sock.send(str.encode(msg))
        else: 
            msg = "No such room found.@"
            print(msg.replace('@',''))
            sock.send(str.encode(msg))
    
    def inform_client(self, tag, roomName, ind):
        # send the member list of a room to a certain client 
        room = list(filter(lambda r: r.roomName == roomName,self.roomList))[0]
        sock = self.memberSockList[ind]
        memberList = '%'.join([m.name for m in room.members]) + '&'
        msg = tag + '#' + roomName + '#' + memberList + '@'
        print("send updated list to member " + str(ind) + ': ' +msg.replace('@','').replace('&',''))
        sock.send(str.encode(msg))

    def log_out(self, sock):
        # end the connection session
        msg = 'Connection is closed from client side.@'
        sock.send(str.encode(msg))
        sock.close()

srv = Room_Server()
