import socket
from Member import memberList
import threading
from queue import Queue
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
        self.endFlag = False
        self.env = {} #{(str)roomName: (str)memberList}
        self.myRoomStates = {} #{(str)roomName: (MemberEventHandler)eventHandler}
        self.updateMsg = Queue()

        updateThd=threading.Thread(target=self.update_env)
        updateThd.setDaemon(1)
        updateThd.start()

        # connect to server
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.s.connect((ip,port))
        ind_msg = self.mem.id + '@'
        self.s.send(str.encode(ind_msg))
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
    
    def get_member_list(self, roomName):
        # get room member list
        # return - (List) room member list
        msg = 'm#'+roomName+ '@'
        self.s.send(str.encode(msg))
        res = self.recv_from_srv(True)
        if(res==''): ret = []
        else: ret = res.split('%')
        # print('Member list for ' + roomName + ': ' + str(ret))
        return ret
    
    def get_room_count(self, roomName):
        # return - (int) number of current members in the given room
        msg = 'n#'+roomName+ '@'
        self.s.send(str.encode(msg))
        ret = self.recv_from_srv(True)
        # print('ret: ' + str(ret))
        return int(ret)

    def create_room(self, name, handler):
        # name - (String) room name
        # send the name of the room you want to create
        msg = 'c#' + name + '#' + self.mem.id + '@'
        self.s.send(str.encode(msg))
        ret = self.recv_from_srv(response=True)
        # print('ret: ' + ret)
        if(ret == 'T'): 
            self.myRoomStates[name] = handler
            print(name + ' has been created.')
        else: print(self.mem.name + ': ' + name + ' has already existed.')
    
    def join_room(self, roomName, handler):
        # roomName - (String) room name
        # send the name of the room you want to join
        msg = 'j#'+roomName+'#'+ self.mem.id+ '@'
        self.s.send(str.encode(msg))
        ret = self.recv_from_srv(response=True)
        if(ret == 'T'): 
            self.myRoomStates[roomName] = handler
            print('You have joined ' + roomName + '.')
        else: print(self.mem.name + ': ' + roomName + ' does not exist or you have already been in the room.')

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
        self.endFlag = True
        self.s.close()

    def reset_handler(self, roomName, handler):
        self.myRoomStates[roomName] = handler
    
    def find_member(self, name = None, id = None):
        if(name): 
            return list(filter(lambda m: m.name == name, memberList))[0]
        if(id):
            return list(filter(lambda m: m.id == id, memberList))[0]
        return None

    def update_env(self):
        while not self.endFlag: 
            if not self.updateMsg.empty():
                msg = self.updateMsg.get()
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
                    newMem = list(set(memberList).difference(prev))
                    for mem in newMem:
                        if(mem != self.mem.name): 
                            print('Finding handler for ' + self.mem.name + ' in ' + roomName + '.')
                            while True:
                                if roomName in self.myRoomStates.keys(): break
                            print('Handler is found for ' + self.mem.name + ' in ' + roomName + '.')
                            memberObj = self.find_member(name=mem)
                            if(memberObj): 
                                self.myRoomStates[roomName].foundNewMember(memberObj)
                                print(str(mem) + ' joins ' + roomName +'!')
                            else: print('No member named ' + mem + ' is found.')
                elif(tag == 'l'):
                    # a member left the room
                    if(roomName in self.env.keys()): 
                        prev = self.env[roomName]
                    else:
                        prev = [] 
                    memLeft = list(set(prev).difference(memberList))
                    for mem in memLeft:
                        if(mem != self.mem.name): 
                            if(roomName in self.myRoomStates.keys()):
                                memberObj = self.find_member(name=mem)
                                if(memberObj): 
                                    self.myRoomStates[roomName].foundLeaveMember(memberObj)
                                    print(str(mem) + ' left ' + roomName +'!')
                                else: print('No member named ' + mem + ' is found.')
                            else: print('No handler is found for ' + self.mem.name + ' in ' + roomName + '.')
                
                self.env[roomName] = memberList
                # print('Update member list for Room ' + roomName + ': ' + str(memberList))
                # print('Current env: ' + str(self.env))

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
            if(not '&' in msg): 
                # no return messages
                print(self.mem.name + ': '+  msg)
            else:
                txt = msg.replace('&', '')
                if('#' in txt):
                    # environment update messages
                    print('update env list for ' + txt)
                    self.updateMsg.put(txt)
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
    