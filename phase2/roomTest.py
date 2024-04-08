from MemberEventHandler import EventHandler
from Member import memberList
from room_client import Room_Client
import sys
import time


def user_action(ind, ip):
    m1 = memberList[ind]
    c1 = Room_Client(m1, ip)

    h1 = EventHandler()
    h2 = EventHandler()
    
    # c1.create_room(m1.name + '\'s Chat Room', h1)
    c1.create_room('Special Room', h2)
    c1.join_room('Special Room', h2)
    c1.get_room_list()
    print("Sleeping......")
    time.sleep(2)
    # num = c1.get_room_count('Special Room')
    # print(str(num) + ' member(s) in Special Room now.')
    # memList = c1.get_member_list('Special Room')
    # print('Member list for Special Room : ' + str(memList))
    # c1.leave_room(m1.name + '\'s Chat Room')
    # c1.leave_room('Chat Room 2')
    c1.leave_room('Special Room')
    c1.get_room_list()
    c1.exit()

### SAMPLE USAGE
# when open the client program, need to choose which user is using, send an index in range [0,9]
if __name__ == '__main__':
    ind = int(sys.argv[1])
    ip = sys.argv[2]
    ## for test
    print(sys.argv)
    user_action(ind, ip)
    
    ## possible user actions: create, join, leave, get room list, exit.
    # m1 = memberList[ind] # member using the program
    # c1 = Room_Client(m1) # create a new client object
    # c1.create_room(m1.name + '\'s Chat Room')
    # c1.leave_room(m1.name + '\'s Chat Room')
    # c1.exit()