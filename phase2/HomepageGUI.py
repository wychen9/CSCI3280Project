import TopCheckGUI
import tkinter as tk
import threading
from tkinter import PhotoImage

class HomepageGUI:

    def __init__(self, EventHandler, client):
        self.eventHandler = EventHandler
        self.client = client
        self.homepageFrame = None
        self.roomListFrame = None
        self.rooms_frame = None
        self.list_canvas = None
        self.root = None
    
    def clickRoom(self, event, roomName, rooms_frame):
        self.eventHandler.setChoosenRoom(roomName)
        event.widget.configure(bg="#FFE699")
        labels = rooms_frame.winfo_children()
        for label in labels:
            if label != event.widget:
                label.configure(bg="#ffffff")

    def newRoom(self, roomName):
        print("New Room: " + roomName)
        room_label = tk.Label(self.rooms_frame, width=70, height=2, text=roomName, font=("Arial", 20), bg="#ffffff", fg="#000000")
        room_label.pack(side=tk.BOTTOM, fill=tk.X, pady=3)
        room_label.bind("<Button-1>", lambda event: self.clickRoom(event, roomName, self.rooms_frame))
        self.list_canvas.update_idletasks()
        self.list_canvas.config(scrollregion=self.list_canvas.bbox("all"))

    def Cancel(self):
        self.eventHandler.stop()
        for widget in self.rooms_frame.winfo_children():
            widget.destroy()
        self.roomListFrame.pack_forget()
        self.homepageFrame.pack(fill=tk.BOTH, expand=True)
        self.homepageFrame.update_idletasks()

    def JoinRoom(self): 
        roomName = self.eventHandler.getChoosenRoom()
        TopCheckGUI.TopCheckBox(self.root, "Join", self.client, roomName)
        self.roomListFrame.pack_forget()
        self.homepageFrame.pack(fill=tk.BOTH, expand=True)
        self.homepageFrame.update_idletasks()

    def CreateCheck(self):
        TopCheckGUI.TopCheckBox(self.root, "Create", self.client)

    def JoinList(self):
        self.homepageFrame.pack_forget()
        self.roomListFrame.pack(fill=tk.BOTH, expand=True)
        self.roomListFrame.update_idletasks()
        self.eventHandler.start()
        roomList = self.client.get_room_list()
        for room in roomList:
            if room != "":
                self.eventHandler.foundNewRoom(room)
                print("Found new room: " + room)

    def createGUI(self):
        self.root = tk.Tk()
        self.root.minsize(1080, 720)
        self.root.title("Online Chat Room")
        self.root.geometry("1080x720")
        self.root.resizable(False, False)
        self.root.configure(bg="#2F5597")
        # Homepage Frame
        self.homepageFrame = tk.Frame(self.root, bg="#2F5597")
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
        self.roomListFrame = tk.Frame(self.root, bg="#2F5597")
        title_label = tk.Label(self.roomListFrame, width=15, height=1, text="Room List", font=("Arial", 30), bg="#2F5597", fg="#ffffff", padx=0, pady=0, borderwidth=0, highlightthickness=0)
        title_label.pack(side=tk.TOP, pady=10)
        list_frame = tk.Frame(self.roomListFrame, width=800, height=450, bg="#BDD7EE", borderwidth=0, highlightthickness=0)
        list_frame.pack(side=tk.TOP, pady=10)

        self.list_canvas = tk.Canvas(list_frame, width=800, height=450, bg="#5B9BD5", borderwidth=0, highlightthickness=0)
        list_scorll = tk.Scrollbar(list_frame, orient=tk.VERTICAL)
        self.rooms_frame = tk.Frame(self.list_canvas, width=800, height=450, bg="#5B9BD5")
        self.list_canvas.create_window((0, 0), window=self.rooms_frame, anchor="nw")
        self.list_canvas.configure(yscrollcommand=list_scorll.set)
        list_scorll.configure(command=self.list_canvas.yview)

        list_scorll.pack(side=tk.RIGHT, fill=tk.Y)
        self.list_canvas.pack(side=tk.LEFT, fill=tk.BOTH)
        

        optionFrame = tk.Frame(self.roomListFrame, bg="#000000")
        optionFrame.pack(side=tk.TOP, pady=5)
        cancel_button = tk.Button(optionFrame, text="Cancel", width=20, height=2, font=("Arial", 20), fg="#000000", borderwidth=50, highlightthickness=0, highlightbackground="#2F5597",command=self.Cancel)
        cancel_button.pack(side=tk.LEFT, padx=0)
        join_button = tk.Button(optionFrame, text="Join", width=20, height=2, font=("Arial", 20), fg="#000000", borderwidth=50, highlightthickness=0, highlightbackground="#2F5597", command=self.JoinRoom)
        join_button.pack(side=tk.RIGHT, padx=0)

        # text_Var.set("Finding Rooms...")
        self.root.mainloop()
