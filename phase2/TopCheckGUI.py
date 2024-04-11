import tkinter as tk
import RoomMeetingGUI
import MemberEventHandler
import audio_client
import multiUsersRecorder
from recording_client import RecordingClient

topbox = None
name_entry = None
romm_name_entry = None
room_name = None
title = None
client = None
root = None

def JoinRoom():
    global root, topbox, name_entry, room_name_entry, room_name, title, client
    if not room_name:
        room_name = room_name_entry.get()
    name = client.mem.getName()
    memberHandler = MemberEventHandler.EventHandler()
    chatRoomRecorder = multiUsersRecorder.ChatRoomRecorder()
    recording_client = RecordingClient(room_name)
    if title == "Create":
        print("Room "+ room_name + " Created!")
        print("Room Creator: " + name)
        client.create_room(room_name, memberHandler)
        audio_client.control("join "+ room_name)
        audio_client.control("open mic")
        topbox.destroy()
        RoomMeetingGUI.createGUI(root, client, room_name, name, memberHandler, chatRoomRecorder, recording_client)
        memberHandler.start()
        print("Start Handler")
        
        

    elif title == "Join":
        print("Room "+ room_name + " Joined!")
        print("Room Joiner: " + name)
        client.join_room(room_name, memberHandler)
        audio_client.control("join "+ room_name)
        audio_client.control("open mic")
        topbox.destroy()
        RoomMeetingGUI.createGUI(root, client, room_name, name, memberHandler, chatRoomRecorder, recording_client)
        memberHandler.start()
        print("Start Handler")
        

def Cancel():
    global topbox
    topbox.destroy()

def TopCheckBox(r, boxTitle, c, roomName=None):
    global root, topbox, name_entry, room_name_entry, room_name, title, client
    title = boxTitle
    client = c
    root = r
    room_name = roomName
    topbox = tk.Toplevel(root)
    topbox.title(boxTitle)
    topbox.geometry("200x150")
    topbox.resizable(False, False)
    topbox.configure(bg="#f2f2f2")

    if boxTitle == "Join":
        empty_label = tk.Label(topbox, width=15, text="", font=("Arial", 6), bg="#F2F2F2", fg="#000000")
        empty_label.pack(side=tk.TOP, pady=0)
        title_label = tk.Label(topbox, width=20, height=1, text="Join Room?", font=("Arial", 20), bg="#f2f2f2", fg="#000000")
        title_label.pack(side=tk.TOP, anchor="nw", pady=10, fill=tk.X)
    if boxTitle == "Create":
        room_name_entry = tk.Entry(topbox, width=30, font=("Arial", 15), bg="#f2f2f2", fg="#000000")
        room_name_entry.pack(side=tk.TOP, pady=5)
        room_name_entry.insert(0, "Room Name")
    # name_entry = tk.Entry(topbox, width=30, font=("Arial", 15), bg="#f2f2f2", fg="#000000")
    # name_entry.pack(side=tk.TOP, pady=5)
    # name_entry.insert(0, "Your Name")
    optionFrame = tk.Frame(topbox)
    optionFrame.pack(side=tk.TOP, pady=20)
    cancel_button = tk.Button(optionFrame, text="Cancel", width=6, height=1, font=("Arial", 15), fg="#000000", bg="#5B9BD5", borderwidth=10, highlightthickness=0, highlightbackground="#F2F2F2", command=Cancel)
    cancel_button.pack(side=tk.LEFT, padx=0)
    join_button = tk.Button(optionFrame, text="Join", width=6, height=1, font=("Arial", 15), fg="#000000", bg="#5B9BD5", borderwidth=10, highlightthickness=0, highlightbackground="#F2F2F2", command=JoinRoom)
    join_button.pack(side=tk.RIGHT, padx=0)
    
