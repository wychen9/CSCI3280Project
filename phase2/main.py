import HomepageGUI
import EventHandler
import audioserver
import audio_client
from phase2.room_client import Room_Client
from Member import memberList

import sys

ind = int(sys.argv[1])
m1 = memberList[ind]
c1 = Room_Client(m1)
# need to know the ip address of the server
audio_client.control("start ip 9808")
eventHandler = EventHandler.EventHandler()
homepageGUI = HomepageGUI.HomepageGUI(eventHandler, c1)
eventHandler.setHomepageGUI(homepageGUI)
homepageGUI.createGUI()
audio_client.control('exit')
c1.exit()
