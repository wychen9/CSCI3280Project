import HomepageGUI
import EventHandler
import audio_client
from room_client import Room_Client
from Member import memberList

import sys

ind = int(sys.argv[1])
ip = "127.0.0.1"
if(len(sys.argv)>2): 
    ip = sys.argv[2]
    ip2 = sys.argv[3]
    ip3 = sys.argv[4]
    # need ip inpu if available

m1 = memberList[ind]
c1 = Room_Client(m1, ip)
# need to know the ip address of the server
audio_client.control("start "+ ip2 +" 9808")
eventHandler = EventHandler.EventHandler()
homepageGUI = HomepageGUI.HomepageGUI(eventHandler, c1, ip3)
eventHandler.setHomepageGUI(homepageGUI)
homepageGUI.createGUI()
audio_client.control('exit')
c1.exit()

