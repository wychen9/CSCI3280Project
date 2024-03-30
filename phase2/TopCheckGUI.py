import tkinter as tk

topbox = None
name_entry = None

def JoinRoom():
    name = name_entry.get()
    #TODO: Turn to Room GUI

def Cancel():
    topbox.destroy()

def TopCheckBox(boxTitle):
    global topbox, name_entry
    topbox = tk.Toplevel()
    topbox.title(boxTitle)
    topbox.geometry("300x200")
    topbox.resizable(False, False)
    topbox.configure(bg="#f2f2f2")

    empty_label = tk.Label(topbox, width=15, text="", font=("Arial", 6), bg="#F2F2F2", fg="#000000")
    empty_label.pack(side=tk.TOP, pady=0)
    title_label = tk.Label(topbox, width=20, height=1, text="Join as", font=("Arial", 20), bg="#f2f2f2", fg="#000000")
    title_label.pack(side=tk.TOP, anchor="nw", pady=10, fill=tk.X)
    name_entry = tk.Entry(topbox, width=30, font=("Arial", 15), bg="#f2f2f2", fg="#000000")
    name_entry.pack(side=tk.TOP, pady=5)
    name_entry.insert(0, "Your Name")
    optionFrame = tk.Frame(topbox)
    optionFrame.pack(side=tk.TOP, pady=20)
    cancel_button = tk.Button(optionFrame, text="Cancel", width=8, height=1, font=("Arial", 15), fg="#000000", bg="#5B9BD5", borderwidth=10, highlightthickness=0, highlightbackground="#F2F2F2", command=Cancel)
    cancel_button.pack(side=tk.LEFT, padx=0)
    join_button = tk.Button(optionFrame, text="Join", width=8, height=1, font=("Arial", 15), fg="#000000", bg="#5B9BD5", borderwidth=10, highlightthickness=0, highlightbackground="#F2F2F2", command=JoinRoom)
    join_button.pack(side=tk.RIGHT, padx=0)
    
