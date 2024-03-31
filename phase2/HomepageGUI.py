import TopCheckGUI
import tkinter as tk
import time
from tkinter import PhotoImage

class HomepageGUI:

    def __init__(self, EventHandler):
        self.eventHandler = EventHandler
        self.homepageFrame = None
        self.roomListFrame = None
        self.rooms_frame = None

    def clickRoom(self, event, roomName):
        self.eventHandler.setChoosenRoom(roomName)
        event.widget.configure(bg="#FFE699")

    def newRoom(self, roomName):
        print("New Room: " + roomName)
        room_label = tk.Label(self.rooms_frame, width=10, height=2, text=roomName, font=("Arial", 20), bg="#ffffff", fg="#000000")
        room_label.pack(side=tk.BOTTOM, fill=tk.X, pady=3)
        room_label.bind("<Button-1>", lambda event: self.clickRoom(roomName))
    
    def Cancel(self):
        self.eventHandler.stop()
        self.roomListFrame.pack_forget()
        self.homepageFrame.pack(fill=tk.BOTH, expand=True)
        self.homepageFrame.update_idletasks()

    #   TODO: join room interface
    def JoinRoom(self): 
        pass

    def CreateCheck(self):
        TopCheckGUI.TopCheckBox("Create a Room")

    def JoinList(self):
        self.homepageFrame.pack_forget()
        self.roomListFrame.pack(fill=tk.BOTH, expand=True)
        self.roomListFrame.update_idletasks()
        self.eventHandler.start()
        self.eventHandler.foundNewRoom("Room1")
        # test
        print("Room1")
        self.eventHandler.foundNewRoom("Room2")
        print("Room2")
        self.eventHandler.foundNewRoom("Room3")
        print("Room3")

    def createGUI(self):
        root = tk.Tk()
        root.minsize(1080, 720)
        root.title("Online Chat Room")
        root.geometry("1080x720")
        root.resizable(False, False)
        root.configure(bg="#2F5597")
        # Homepage Frame
        self.homepageFrame = tk.Frame(root, bg="#2F5597")
        self.homepageFrame.pack(fill=tk.BOTH, expand=True)
        empty_label = tk.Label(self.homepageFrame, width=15, height=1, text="", font=("Arial", 60), bg="#2F5597", fg="#2F5597")
        empty_label.pack(side=tk.TOP, pady=5)
        title_label = tk.Label(self.homepageFrame, width=15, height=2, text="Online Chat Room", font=("Arial", 60), bg="#2F5597", fg="#ffffff", padx=0, pady=0, borderwidth=0, highlightthickness=0)
        title_label.pack(side=tk.TOP, pady=50)
        create_button = tk.Button(self.homepageFrame, text="Create", width=15, height=2, font=("Arial", 23), bg="#ffffff", fg="#000000", padx=0, pady=0, borderwidth=0, highlightthickness=0, command=self.CreateCheck)
        create_button.pack(side=tk.TOP, pady=0)
        join_button = tk.Button(self.homepageFrame, text="Join a Room", width=15, height=2, font=("Arial", 23), bg="#ffffff", fg="#000000", padx=0, pady=0, borderwidth=0, highlightthickness=0, command=self.JoinList)
        join_button.pack(side=tk.TOP, pady=40)

        # Room List Frame
        self.roomListFrame = tk.Frame(root, bg="#2F5597")
        title_label = tk.Label(self.roomListFrame, width=15, height=1, text="Room List", font=("Arial", 30), bg="#2F5597", fg="#ffffff", padx=0, pady=0, borderwidth=0, highlightthickness=0)
        title_label.pack(side=tk.TOP, pady=10)
        list_frame = tk.Frame(self.roomListFrame, width=800, height=500, bg="#BDD7EE")
        list_frame.pack(side=tk.TOP, pady=10)

        list_canvas = tk.Canvas(list_frame, width=800, height=500, bg="#BDD7EE", borderwidth=0, highlightthickness=0)
        list_scorll = tk.Scrollbar(list_frame, orient=tk.VERTICAL, command=list_canvas.yview)
        self.rooms_frame = tk.Frame(list_canvas, bg="#BDD7EE")
        list_canvas.create_window((0, 0), window=self.rooms_frame, anchor="nw")
        list_canvas.configure(yscrollcommand=list_scorll.set)

        list_canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        list_scorll.pack(side=tk.RIGHT, fill=tk.Y)
        self.rooms_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        optionFrame = tk.Frame(self.roomListFrame, bg="#000000")
        optionFrame.pack(side=tk.TOP, pady=5)
        cancel_button = tk.Button(optionFrame, text="Cancel", width=20, height=10, font=("Arial", 15), fg="#000000", borderwidth=50, highlightthickness=0, highlightbackground="#2F5597",command=self.Cancel)
        cancel_button.pack(side=tk.LEFT, padx=0)
        join_button = tk.Button(optionFrame, text="Join", width=20, height=10, font=("Arial", 15), fg="#000000", borderwidth=50, highlightthickness=0, highlightbackground="#2F5597", command=self.JoinRoom)
        join_button.pack(side=tk.RIGHT, padx=0)

        # text_Var.set("Finding Rooms...")
        root.mainloop()
