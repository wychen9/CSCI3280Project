import HomepageGUI
import EventHandler
from client import Client
from Member import memberList
import sys

ind = int(sys.argv[1])
m1 = memberList[ind]
c1 = Client(m1)
eventHandler = EventHandler.EventHandler()
homepageGUI = HomepageGUI.HomepageGUI(eventHandler, c1)
eventHandler.setHomepageGUI(homepageGUI)
homepageGUI.createGUI()
c1.exit()
