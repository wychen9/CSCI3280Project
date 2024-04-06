from queue import Queue
from threading import Thread
import RoomMeetingGUI

class EventHandler:
    def __init__(self):
        self.queue = Queue()
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
            
    def foundNewMember(self, member):
        self.queue.put(member)