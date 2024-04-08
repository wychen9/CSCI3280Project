import socket
from Member import memberList
import threading
from queue import Queue
import time
import os
#  CHAT ROOM NAME CANNOT CONTAIN '&', '%', '#' and '@' !!!
ip = '127.0.0.1'

class Room_Client():
    def __init__(self, mem, ip, port = 8888):
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
        self.recvLock = threading.Lock()
        self.thds= []

        self.port = port
        self.ip = ip

        # connect to server
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.s.connect((self.ip,self.port))
        self.s.settimeout(0.0)
        ind_msg = self.mem.id + '@'
        self.s.send(str.encode(ind_msg))

        self.thds.append(threading.Thread(target=self.recv_updates))
        self.thds.append(threading.Thread(target=self.update_env))
        for thd in self.thds:
            thd.setDaemon(1)
            thd.start()
    
    def recv_updates(self):
        while not self.endFlag:
            try:
                locked = self.recvLock.acquire(blocking=False)
                if locked:
                    try:
                        ret = self.s.recv(1024, socket.MSG_PEEK).decode('utf-8')
                        if(ret[0] == 'j' or ret[0] == 'l'): self.recv_from_srv()
                    except Exception as e:
                        continue    
            finally:
                if locked:
                    self.recvLock.release()
            # print('in recv_updates')
            time.sleep(0.1)
        # print('recv_updates end')
    
    def get_room_list(self):
        # get current room list
        # return - (List) current room list
        self.recvLock.acquire()
        msg = 'r@'
        self.s.send(str.encode(msg))
        res = self.recv_from_srv(True)
        self.recvLock.release()
        if(res==''): self.roomList = []
        else: self.roomList = res.split('%')
        print('roomList for ' + self.mem.name + ': ' + str(self.roomList))
        return self.roomList
    
    def get_member_list(self, roomName):
        # get room member list
        # return - (List) room member list
        self.recvLock.acquire()
        msg = 'm#'+roomName+ '@'
        self.s.send(str.encode(msg))
        res = self.recv_from_srv(True)
        self.recvLock.release()
        if(res==''): ret = []
        else: ret = res.split('%')
        # print('Member list for ' + roomName + ': ' + str(ret))
        return ret
    
    def get_room_count(self, roomName):
        self.recvLock.acquire()
        # return - (int) number of current members in the given room
        msg = 'n#'+roomName+ '@'
        self.s.send(str.encode(msg))
        ret = self.recv_from_srv(True)
        self.recvLock.release()
        # print('ret: ' + str(ret))
        return int(ret)

    def create_room(self, name, handler):
        # name - (String) room name
        # send the name of the room you want to create
        self.recvLock.acquire()
        msg = 'c#' + name + '#' + self.mem.id + '@'
        self.s.send(str.encode(msg))
        ret = self.recv_from_srv(response=True)
        self.recvLock.release()
        print('ret: ' + str(ret))
        if(ret == 'T'): 
            self.myRoomStates[name] = handler
            print(name + ' has been created.')
        else: print(self.mem.name + ': ' + name + ' has already existed.')
    
    def join_room(self, roomName, handler):
        # roomName - (String) room name
        # send the name of the room you want to join
        self.recvLock.acquire()
        msg = 'j#'+roomName+'#'+ self.mem.id+ '@'
        self.s.send(str.encode(msg))
        ret = self.recv_from_srv(response=True)
        self.recvLock.release()
        if(ret == 'T'): 
            self.myRoomStates[roomName] = handler
            print('You have joined ' + roomName + '.')
        else: print(self.mem.name + ': ' + roomName + ' does not exist or you have already been in the room.')

    def leave_room(self, roomName):
        # roomName - (String) room name
        # send the name of the room you want to leave
        self.recvLock.acquire()
        msg = 'l#'+roomName+'#'+ self.mem.id+ '@'
        self.s.send(str.encode(msg))
        self.recvLock.release()
    
    def exit(self):
        # exit the program and close the connection with the server
        self.recvLock.acquire()
        msg = 'e@'
        self.s.send(str.encode(msg))
        self.recvLock.release()
        self.endFlag = True
        self.recv_from_srv()
        self.s.close()
        for thd in self.thds:
            thd.join()
        print('Client exit() completed')

    def reset_handler(self, roomName, handler):
        self.myRoomStates[roomName] = handler
    
    def find_member(self, name = None, id = None):
        if(name): 
            return list(filter(lambda m: m.name == name, memberList))[0]
        if(id):
            return list(filter(lambda m: m.id == id, memberList))[0]
        return None

    def update_env(self):
        while (not self.endFlag) or (not self.updateMsg.empty()): 
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
        # print('Update_env end')

    def preview_recv(self, response = False):
        try: 
            # time.sleep(1)
            d = self.s.recv(1024, socket.MSG_PEEK).decode('utf-8')
            msgs = list(filter(lambda x: x!= '', d.split('@')))
        except Exception as e:
            return None
        else: 
            if(not response): return 1024
            else:
                bufSize = 0
                for ind in range(len(msgs)):
                    bufSize += len(msgs[ind]) + 1
                    if('&' in msgs[ind] and not '#' in msgs[ind]): return bufSize
                return None
            
    def recv_from_srv(self, response = False):
        # j#roomName#memberList@ - Update on member joining current room
        # l#roomName#memberList@ - Update on member leaving current room
        # 
        while True:
            if (d:=self.preview_recv(response)): break
        msgs = self.s.recv(d).decode('utf-8').split('@')
        msgs = list(filter(lambda x: x!= '', msgs))
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
                    return msg.replace('&', '')
        
    def upload_file(self, room_name, file_path):

        if not os.path.isfile(file_path):
            print(f"File not found: {file_path}.")
            return
        
        # Lock the thread to send data to server
        self.recvLock.acquire()

        try:
            # extract the file name from the file path
            file_name = os.path.basename(file_path)
            # read the file in binary mode
            with open (file_path, 'rb') as file:
                file_data = file.read()
            
            # create a msg for file upload
            msg = f'u#{room_name}#{file_name}@{file_data}'

            self.s.sendall(str.encode(msg))

            ret = self.recv_from_srv(response=True)
                #lock released

            if ret == 'T':
                print(f"File {file_name} has been uploaded to {room_name}.")
            else:
                print(f'Failed to upload file to {room_name}. Server response: {ret}')
        
        finally:
            # always release the lock, even if an error occurred
            self.recvLock.release()

        # try: 
        #     # time.sleep(1)
        #     d = self.s.recv(1024, socket.MSG_PEEK).decode('utf-8')
        # except Exception as e:
        #     print(e)
        #     if(response): return self.recv_from_srv(True)
        #     else: return
        # else:
        #     if(response): 
        #         if(not '&' in d): return self.recv_from_srv(True)


        # buffer = list(filter(lambda x: x!= '', d.split('@')))
        # ind = 0
        # bufSize = 0
            # try: 
            #     if(response):
            #         while(not '&' in buffer[ind] or buffer[ind][0] == 'j' or buffer[ind][0] == 'l'):
            #             bufSize += len(buffer[ind]) + 1
            #             ind += 1
            #     else:
            #         while(buffer[ind][0] == 'j' or buffer[ind][0] == 'l'):
            #             bufSize += len(buffer[ind]) + 1
            #             ind += 1
            # except Exception as e:
            #     if(response): return self.recv_from_srv(True)
            #     else: return
        # if(response):
        #     while(not '&' in buffer[ind] or buffer[ind][0] == 'j' or buffer[ind][0] == 'l'):
        #         bufSize += len(buffer[ind]) + 1
        #         ind += 1
        # else:
        #     while(buffer[ind][0] == 'j' or buffer[ind][0] == 'l'):
        #         bufSize += len(buffer[ind]) + 1
        #         ind += 1

        # print('buffer: ' + str(buffer))
        # print('msgs: '+ str(msgs))


            # buffer.append(d)
            # data = b''.join(buffer)
            # msg = str(data,'UTF-8')
            # msgs = list(filter(lambda x: x!= '', msgs))
            # for msg in msgs:
            #     if(not '&' in msg): print(self.mem.name + ': '+  msg)
            # print('msgs: ' + str(msgs))
            # print('msg: '+ msg)
            # for msg in msgs:
            #     if(not '&' in msg): 
            #         # no return messages
            #         print(self.mem.name + ': '+  msg)
            #     else:
            #         txt = msg.replace('&', '')
            #         if('#' in txt):
            #             # environment update messages
            #             print('update env list for ' + txt)
            #             self.updateMsg.put(txt)
            #         else:
            #             filteredM.append(txt)
            # if(response):
            #     # print('filteredM: ' + str(filteredM))
            #     if(len(filteredM)>0): 
            #         # print('remaining msgs: ' + str(filteredM))
            #         return filteredM[0]
            #     else:
            #         return self.recv_from_srv(True)
            #         # buffer = []
            #         # d = self.s.recv(1024)
            #         # buffer.append(d)
            #         # data = b''.join(buffer)
            #         # msg = str(data,'UTF-8')

            #         # return msg.replace('@', '').replace('&', '')

            #         # return msg.replace('@', '').replace('&', '')
