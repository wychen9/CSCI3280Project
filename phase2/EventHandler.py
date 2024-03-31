from queue import Queue
from threading import Thread
import tkinter as tk
import HomepageGUI

class EventHandler:
    def __init__(self):
        self.queue = Queue()
        self.isActive = False
        self.thread = Thread(target=self.run)
        self.roomNameChoosen = None
        self.stopThreads = False
        self.homepageGUI = None
        self.firstStart = True
    def start(self):
        self.isActive = True
        if self.firstStart:
            self.thread.start()
    
    def stop(self):
        self.isActive = False
        self.firstStart = False
    
    def run(self):
        while self.isActive:
            print("Thread is running")
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