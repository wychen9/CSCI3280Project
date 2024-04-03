import HomepageGUI
import EventHandler
from room_client import Room_Client
from Member import memberList
import sys

ind = int(sys.argv[1])
m1 = memberList[ind]
c1 = Room_Client(m1)
eventHandler = EventHandler.EventHandler()
homepageGUI = HomepageGUI.HomepageGUI(eventHandler, c1)
eventHandler.setHomepageGUI(homepageGUI)
homepageGUI.createGUI()
