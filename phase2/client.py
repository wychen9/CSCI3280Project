from Room import Room
import socket
#  CHAT ROOM NAME CANNOT CONTAIN '&', '%', '#' and '@' !!!
ip = '127.0.0.1'
port = 8888

class Client():
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
        self.env = {} #{(str)roomName: (str)memberList}

        # connect to server
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.s.connect((ip,port))
        ind_msg = self.mem.id + '@'
        self.s.send(str.encode(ind_msg))
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
        res = self.recv_from_srv(True)
        if(res==''): self.roomList = []
        else: self.roomList = res.split('%')
        print('roomList for ' + self.mem.name + ': ' + str(self.roomList))
        return self.roomList
    
    def get_room_count(self, roomName):
        # return - (int) number of current members in the given room
        msg = 'n#'+roomName+ '@'
        self.s.send(str.encode(msg))
        ret = self.recv_from_srv(True)
        # print('ret: ' + str(ret))
        return int(ret)

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

    def update_env(self, msg):
        # print(msg)
        [tag, roomName, memberList] = msg.split('#')
        memberList = memberList.split('%')
        # if(isinstance(memberList, str)): memberList = [memberList]
        if(tag == 'j'):
            # new member joining the room
            if(roomName in self.env.keys()): 
                prev = self.env[roomName]
            else: 
                prev = []
            print(str(set(memberList).difference(prev)) + ' joins ' + roomName +'!')
            
        elif(tag == 'l'):
            # a member left the room
            if(roomName in self.env.keys()): 
                prev = self.env[roomName]
            else:
                prev = []
                
            print(str(set(prev).difference(memberList)) + ' left ' + roomName +'!')
        
        self.env[roomName] = memberList
        # print('Update member list for Room ' + roomName + ': ' + str(memberList))
        # print('Current env: ' + str(self.env))
        return self.roomList

    def recv_from_srv(self, response = False):
        # j#roomName#memberList@ - Update on member joining current room
        # l#roomName#memberList@ - Update on member leaving current room
        # 
        buffer = []
        d = self.s.recv(1024)
        buffer.append(d)
        data = b''.join(buffer)
        msg = str(data,'UTF-8')
        # msgs = list(filter(lambda x: x!= '', msgs))
        # for msg in msgs:
        #     if(not '&' in msg): print(self.mem.name + ': '+  msg)
        msgs = list(filter(lambda x: x!= '', msg.split('@')))
        filteredM = []

        # print('msgs: ' + str(msgs))
        
        for msg in msgs:
            if(not '&' in msg): print(self.mem.name + ': '+  msg)
            else:
                txt = msg.replace('&', '')
                if('#' in txt):
                    self.update_env(txt)
                    msgs.remove(msg)
                else:
                    filteredM.append(txt)
        if(response):
            # print('filteredM: ' + str(filteredM))
            if(len(filteredM)>0): 
                # print('remaining msgs: ' + str(filteredM))
                return filteredM[0]
            else:
                return self.recv_from_srv(True)
                # buffer = []
                # d = self.s.recv(1024)
                # buffer.append(d)
                # data = b''.join(buffer)
                # msg = str(data,'UTF-8')

                # return msg.replace('@', '').replace('&', '')