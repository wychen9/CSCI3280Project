import tkinter as tk
import MemberEventHandler

root, roomTopLevel = None, None
client = None
memberHandler = None
room_name, count, isFirst = None, None, True
member_canvas, member_scorll_frame = None, None
mute_var, record_var, status_var = None, None, None
circle_canvas, circle = None, None

def createMember(name, i, j):
    global member_canvas, member_scorll_frame, circle_canvas, circle, count
    member_frame = tk.Frame(member_scorll_frame, width=280, height=220, bg="grey", borderwidth=0, highlightthickness=0)
    member_frame.grid(row=i, column=j, padx=30, pady=10)
    video_frame = tk.Frame(member_frame, width=280, height=180, bg="green", borderwidth=0, highlightthickness=0)
    video_frame.pack(side=tk.TOP, fill=tk.X)
    video_frame.pack_propagate(False)
    status_frame = tk.Frame(member_frame, width=280, height=40, bg="#ffffff", borderwidth= 0, highlightthickness=0)
    status_frame.pack(side=tk.BOTTOM, fill=tk.X)
    status_frame.pack_propagate(False)
    name_label = tk.Label(status_frame, width=10, height=1, text=name, font=("Arial", 15), bg="#ffffff", fg="black")
    name_label.place(relx=0.5, rely=0.5, anchor="center")
    mute_canvas = tk.Canvas(status_frame, width=30, height=30, bg="#ffffff", borderwidth=0, highlightthickness=0)
    mute_canvas.place(relx=0.5, rely=0.5, anchor="e", x=-50)
    oval = mute_canvas.create_oval(7, 7, 23, 23, fill="red", outline="white")
    if count == i*3 + j:
        circle_canvas = mute_canvas
        circle = oval
    member_canvas.update_idletasks()
    member_canvas.config(scrollregion=member_canvas.bbox("all"))

def newMember(member):
    global client, room_name
    c = client.get_room_count(room_name)
    i = c // 3
    j = c % 3
    createMember(member, i, j)

# --------------------------------------------------------------
# TODO: Mute or unmute
# --------------------------------------------------------------
def MuteOrUnmute():
    global mute_var, circle_canvas, circle
    if mute_var.get() == "Mute":
        mute_var.set("Unmute")
        circle_canvas.itemconfig(circle, fill="#ffffff")
    else:
        mute_var.set("Mute")
        circle_canvas.itemconfig(circle, fill="red")

# --------------------------------------------------------------
# TODO: Start or stop recording
# --------------------------------------------------------------
def StartOrStopRecord():
    global record_var, status_var
    if record_var.get() == "Start Record":
        record_var.set("Stop Record")
        status_var.set("Recording...")
    else:
        record_var.set("Start Record")
        status_var.set("")

# --------------------------------------------------------------
# TODO: Download recording file
# --------------------------------------------------------------
def downloadRecording():
    print("Download recording")

def startHandler(event):
    global memberHandler, isFirst
    if isFirst:
        memberHandler = MemberEventHandler.EventHandler()
        memberHandler.start()
        print("Start Handler")
        isFirst = False

def Quit():
    global root, client, room_name, memberHandler, roomTopLevel
    client.leave_room(room_name)
    memberHandler.stop()
    print("Stop Handler")
    roomTopLevel.destroy()

def createGUI(r, c, roomName, name):
    global root, client, room_name, count, member_canvas, member_scorll_frame, roomTopLevel
    global mute_var, record_var, status_var
    root = r
    client = c
    room_name = roomName
    roomTopLevel = tk.Toplevel(root)
    roomTopLevel.bind("<Map>", startHandler)
    roomTopLevel.minsize(1080, 720)
    roomTopLevel.title("Online Chat Room")
    roomTopLevel.geometry("1080x720")
    roomTopLevel.resizable(False, False)
    roomTopLevel.configure(bg="grey")
    # Menu
    menubar = tk.Menu(roomTopLevel)
    options_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Option", menu=options_menu)
    options_menu.add_command(label="Download Recording", command=downloadRecording)
    options_menu.add_separator()
    options_menu.add_command(label="Exit", command=Quit)
    roomTopLevel.config(menu=menubar)

    # Room Meeting Frame
    roomMeetingFrame = tk.Frame(roomTopLevel, bg="grey")
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
    record_var.set("Start Record")
    status_var.set("")
    mute_var.set("Mute")

    # --------------------------------------------------------------
    # TODO: Get members'name in the room to set the GUI
    # --------------------------------------------------------------
    count = client.get_room_count(roomName)
    tmp = count
    while tmp > 0:
        i = tmp // 3
        j = tmp % 3
        createMember(name, i, j)
        tmp -= 1

    roomTopLevel.protocol("WM_DELETE_WINDOW", Quit)