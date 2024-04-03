from room_client import Room_Client
import sys
import time
NUM_OF_USER = 10
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

# Predefined 10 users
memberList = [] 
for i in range(0,NUM_OF_USER):
    member = Member('User ' + str(i))
    member.setID(str(i))
    memberList.append(member)

# def user_action(ind):
#     m1 = memberList[ind]
#     c1 = Room_Client(m1)
    
#     c1.create_room(m1.name + '\'s Chat Room')
#     c1.create_room('Chat Room 2')
#     c1.create_room('Special Room')
#     c1.join_room('Special Room')
#     c1.join_room('Chat Room 2')
#     c1.get_room_list()
#     print("Sleeping......")
#     time.sleep(10)
#     c1.leave_room(m1.name + '\'s Chat Room')
#     c1.leave_room('Chat Room 2')
#     c1.leave_room('Special Room')
#     c1.get_room_list()
#     c1.exit()

# ### SAMPLE USAGE
# # when open the client program, need to choose which user is using, send an index in range [0,9]
# if __name__ == '__main__':
#     ind = int(sys.argv[1])
#     ## for test
#     user_action(ind)
    
#     ## possible user actions: create, join, leave, get room list, exit.
#     # m1 = memberList[ind] # member using the program
#     # c1 = Room_Client(m1) # create a new client object
#     # c1.create_room(m1.name + '\'s Chat Room')
#     # c1.leave_room(m1.name + '\'s Chat Room')
#     # c1.exit()

