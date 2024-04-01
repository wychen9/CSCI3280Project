from queue import Queue
from threading import Thread

class EventHandler:
    def __init__(self):
        self.queue = Queue()
        self.isActive = False
        self.thread = None
        self.roomNameChoosen = None
        self.stopThreads = False
        self.homepageGUI = None
    
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
                roomName = self.queue.get()
                self.homepageGUI.newRoom(roomName)
            
    def foundNewRoom(self, roomName):
        self.queue.put(roomName)

    def setChoosenRoom(self, roomName):
        self.roomNameChoosen = roomName

    def getChoosenRoom(self):
        return self.roomNameChoosen
    
    def setHomepageGUI(self, homepageGUI):
        self.homepageGUI = homepageGUI