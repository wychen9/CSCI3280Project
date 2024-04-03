import tkinter as tk

root, member_canvas, member_scorll_frame = None, None, None
mute_var, record_var, status_var = None, None, None
def createMember(name, i, j):
    member_frame = tk.Frame(member_scorll_frame, width=280, height=220, bg="grey", borderwidth=0, highlightthickness=0)
    member_frame.grid(row=i, column=j, padx=30, pady=10)
    video_frame = tk.Frame(member_frame, width=280, height=180, bg="green", borderwidth=0, highlightthickness=0)
    video_frame.pack(side=tk.TOP, fill=tk.X)
    video_frame.pack_propagate(False)
    status_frame = tk.Frame(member_frame, width=280, height=40, bg="#ffffff", borderwidth= 0, highlightthickness=0)
    status_frame.pack(side=tk.BOTTOM, fill=tk.X)
    status_frame.pack_propagate(False)
    name_label = tk.Label(status_frame, width=5, height=1, text=name, font=("Arial", 15), bg="#ffffff", fg="black")
    name_label.place(relx=0.5, rely=0.5, anchor="center")
    mute_canvas = tk.Canvas(status_frame, width=30, height=30, bg="#ffffff", borderwidth=0, highlightthickness=0)
    mute_canvas.place(relx=0.5, rely=0.5, anchor="e", x=-50)
    mute_canvas.create_oval(7, 7, 23, 23, fill="red", outline="white")
    member_canvas.update_idletasks()
    member_canvas.config(scrollregion=member_canvas.bbox("all"))

def MuteOrUnmute():
    if mute_var.get() == "Mute":
        mute_var.set("Unmute")
    else:
        mute_var.set("Mute")

def StartOrStopRecord():
    if record_var.get() == "Start Record":
        record_var.set("Stop Record")
        status_var.set("Recording...")
    else:
        record_var.set("Start Record")
        status_var.set("")

def downloadRecording():
    print("Download recording")

def Quit():
    root.quit()

def createGUI(client, roomName, name):
    global root, member_canvas, member_scorll_frame
    global mute_var, record_var, status_var
    root = tk.Tk()
    root.minsize(1080, 720)
    root.title("Online Chat Room")
    root.geometry("1080x720")
    root.resizable(False, False)
    root.configure(bg="grey")
    # Menu
    menubar = tk.Menu(root)
    options_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Option", menu=options_menu)
    options_menu.add_command(label="Download Recording", command=downloadRecording)
    options_menu.add_separator()
    options_menu.add_command(label="Exit", command=Quit)
    root.config(menu=menubar)

    # Room Meeting Frame
    roomMeetingFrame = tk.Frame(root, bg="grey")
    roomMeetingFrame.pack(fill=tk.BOTH, expand=True)

    # Top——Room Name
    top_frame = tk.Frame(roomMeetingFrame, width=1080, height=100, bg="#ffffff", borderwidth=0, highlightthickness=0)
    top_frame.pack(side=tk.TOP, fill=tk.X)
    roomName_label = tk.Label(top_frame, width=10, height=2, text=roomName, font=("Arial", 20), bg="#2F5597", fg="#ffffff")
    roomName_label.pack(side=tk.TOP, fill=tk.BOTH, pady=2)
    status_var = tk.StringVar()
    status_label = tk.Label(top_frame, width=10, height=2, textvariable=status_var, font=("Arial", 15), bg="#ffffff", fg="red")
    status_label.pack(side=tk.TOP, fill=tk.BOTH, pady=2)

    # Bottom——Mute & Record
    bottom_frame = tk.Frame(roomMeetingFrame, width=1080, height=100, bg="#2F5597")
    bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)
    bottom_frame.pack_propagate(False)
    mute_var = tk.StringVar()
    mute_button = tk.Button(bottom_frame, textvariable=mute_var, width=10, height=2, font=("Arial", 15), bg="#2F5597", fg="#000000", padx=0, pady=0, borderwidth=0, highlightthickness=0, command=MuteOrUnmute)
    mute_button.pack(side=tk.LEFT, padx=50, pady=20)
    record_var = tk.StringVar()
    record_button = tk.Button(bottom_frame, textvariable=record_var, width=10, height=2, font=("Arial", 15), bg="#2F5597", fg="#000000", padx=0, pady=0, borderwidth=0, highlightthickness=0, command=StartOrStopRecord)
    record_button.pack(side=tk.RIGHT, padx=50, pady=20)

    # Middle——Chat Room
    middle_frame = tk.Frame(roomMeetingFrame, width=1080, height=1000, bg="#ffffff")
    middle_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    member_canvas = tk.Canvas(middle_frame, width=1080, height=1000, bg="#ffffff", borderwidth=0, highlightthickness=0)
    member_scorll = tk.Scrollbar(middle_frame, orient="vertical", command=member_canvas.yview)
    member_scorll_frame = tk.Frame(member_canvas, width=1200, height=1000, bg="#ffffff")
    member_canvas.create_window((0, 0), window=member_scorll_frame, anchor="nw")
    member_canvas.configure(yscrollcommand=member_scorll.set)
    member_scorll.pack(side=tk.RIGHT, fill=tk.Y)
    member_canvas.pack(side=tk.LEFT, fill=tk.BOTH)

    # set text
    mute_var.set("Mute")
    record_var.set("Start Record")
    status_var.set("")

    # test
    createMember(name, 0, 0)


    root.mainloop()