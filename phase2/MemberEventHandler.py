from queue import Queue
from threading import Thread
import RoomMeetingGUI

class EventHandler:
    def __init__(self):
        self.queue = Queue()
        self.leaveQueue = Queue()
        self.isActive = False
        self.thread = None
    
    def start(self):
        self.isActive = True
        self.thread = Thread(target=self.run)
        self.thread.start()      
        
    def stop(self):
        self.isActive = False
        self.thread.join()

    def run(self):
        while self.isActive:
            if self.queue.empty() is not True:
                member = self.queue.get()
                RoomMeetingGUI.newMember(member)
                print("Handler: New member found!")
            if self.leaveQueue.empty() is not True:
                member = self.leaveQueue.get()
                RoomMeetingGUI.leaveMember(member)
                print("Handler: New member leave!")
            
    def foundNewMember(self, member):
        self.queue.put(member)

    def foundLeaveMember(self, member):
        self.leaveQueue.put(member)