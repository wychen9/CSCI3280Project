from room_client import Room_Client
import sys
import time
NUM_OF_THD = 3

class Member:
    def __init__(self, name):
        self.id = None
        self.name = name
    
    def setID(self, id):
        self.id = id
    
    def getID(self):
        return self.id

    def getName(self):
        return self.name

memberList = [] 
for i in range(0,10):
    member = Member('User ' + str(i))
    member.setID(str(i))
    memberList.append(member)

def user_action(ind):
    m1 = memberList[ind]
    c1 = Room_Client(m1)
    c1.create_room(m1.name + '\'s Chat Room')
    c1.create_room('Chat Room 2')
    c1.create_room('Special Room')
    c1.join_room('Special Room')
    c1.join_room('Chat Room 2')
    c1.get_room_list()
    print("Sleeping......")
    time.sleep(10)
    c1.leave_room(m1.name + '\'s Chat Room')
    c1.leave_room('Chat Room 2')
    c1.leave_room('Special Room')
    c1.get_room_list()
    c1.end_connect()

if __name__ == '__main__':
    ind = int(sys.argv[1])
    user_action(ind)