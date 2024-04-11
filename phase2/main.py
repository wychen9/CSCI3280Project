import HomepageGUI
import EventHandler
import audio_client
from recording_server import RecordingServer
from recording_client import RecordingClient
from room_client import Room_Client
from Member import memberList

import sys

ind = int(sys.argv[1])
ip = "127.0.0.1"
if(len(sys.argv)>2): 
    ip = sys.argv[2]
    ip2 = sys.argv[3]
    # need ip inpu if available
recording_server = RecordingServer()

m1 = memberList[ind]
c1 = Room_Client(m1, ip)
# need to know the ip address of the server
audio_client.control("start "+ ip2 +" 9808")
recording_client = RecordingClient(c1.get_room_name())
eventHandler = EventHandler.EventHandler()
homepageGUI = HomepageGUI.HomepageGUI(eventHandler, c1)
eventHandler.setHomepageGUI(homepageGUI)
homepageGUI.createGUI()
audio_client.control('exit')
c1.exit()

