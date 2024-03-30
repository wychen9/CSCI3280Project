import TopCheckGUI
import tkinter as tk
from tkinter import PhotoImage

root = tk.Tk()
root.minsize(1080, 720)
root.title("Online Chat Room")
root.geometry("1080x720")
root.resizable(False, False)
root.configure(bg="#2F5597")

def Cancel():
    roomListFrame.pack_forget()
    homepageFrame.pack(fill=tk.BOTH, expand=True)
    homepageFrame.update_idletasks()

def JoinRoom(): 
    pass

def CreateCheck():
    TopCheckGUI.TopCheckBox("Create a Room")

def JoinList():
    homepageFrame.pack_forget()
    roomListFrame.pack(fill=tk.BOTH, expand=True)
    roomListFrame.update_idletasks()

homepageFrame = tk.Frame(root, bg="#2F5597")
homepageFrame.pack(fill=tk.BOTH, expand=True)
empty_label = tk.Label(homepageFrame, width=15, height=1, text="", font=("Arial", 60), bg="#2F5597", fg="#2F5597")
empty_label.pack(side=tk.TOP, pady=5)
title_label = tk.Label(homepageFrame, width=15, height=2, text="Online Chat Room", font=("Arial", 60), bg="#2F5597", fg="#ffffff", padx=0, pady=0, borderwidth=0, highlightthickness=0)
title_label.pack(side=tk.TOP, pady=50)
create_button = tk.Button(homepageFrame, text="Create", width=15, height=2, font=("Arial", 23), bg="#ffffff", fg="#000000", padx=0, pady=0, borderwidth=0, highlightthickness=0, command=CreateCheck)
create_button.pack(side=tk.TOP, pady=0)
join_button = tk.Button(homepageFrame, text="Join a Room", width=15, height=2, font=("Arial", 23), bg="#ffffff", fg="#000000", padx=0, pady=0, borderwidth=0, highlightthickness=0, command=JoinList)
join_button.pack(side=tk.TOP, pady=40)

roomListFrame = tk.Frame(root, bg="#2F5597")
title_label = tk.Label(roomListFrame, width=15, height=1, text="Room List", font=("Arial", 30), bg="#2F5597", fg="#ffffff", padx=0, pady=0, borderwidth=0, highlightthickness=0)
title_label.pack(side=tk.TOP, pady=10)
list_canvas = tk.Canvas(roomListFrame, width=800, height=500, bg="#BDD7EE")
optionFrame = tk.Frame(roomListFrame)
optionFrame.pack(side=tk.TOP, pady=10)
cancel_button = tk.Button(optionFrame, text="Cancel", width=8, height=1, font=("Arial", 15), fg="#000000", borderwidth=10, highlightthickness=0, highlightbackground="#F2F2F2",command=Cancel)
cancel_button.pack(side=tk.LEFT, padx=0)
join_button = tk.Button(optionFrame, text="Join", width=8, height=1, font=("Arial", 15), fg="#000000", borderwidth=10, highlightthickness=0, highlightbackground="#F2F2F2", command=JoinRoom)
join_button.pack(side=tk.RIGHT, padx=0)

root.mainloop()
