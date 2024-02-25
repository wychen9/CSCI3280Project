import tkinter as tk
from tkinter import PhotoImage
from tkinter import ttk

click = 0
isPlaying = False
audioLength = 100

root = tk.Tk()
root.title("Video Recorder")
root.geometry("1080x720")
root.resizable(width=False, height=False)

# import images
modifyImage = PhotoImage(file="images/Modify.PNG")
startImage = PhotoImage(file="images/Start.PNG")
pauseImage = PhotoImage(file="images/Pause.PNG")
replaceImage = PhotoImage(file="images/Replace.PNG")

# set style
style = ttk.Style(root)
style.theme_use("default")
style.configure("TCombobox", foreground="#000000", background="BFBFBF")

# define functions
def on_combobox_select(event):
    # selected_value = speedCombo.get()
    root.after(0, lambda: speedCombo.selection_clear())

def DISABLED(event):
    print("click")
    return 

def StartOrPauseChange(event):
    global click, startOrPauseCanvas, startOrPauseButton
    if click % 2 == 0:
        startOrPauseCanvas.itemconfig(startOrPauseButton, image=pauseImage)
        isPlaying = True
        print("playing")
    else:
        startOrPauseCanvas.itemconfig(startOrPauseButton, image=startImage)
        isPlaying = False
        print("stopping")
    click += 1

def moveOnClick(event):
    global curX, processCanvas, processCircle
    processCanvas.tag_raise(processCircle)
    curX= event.x 

def moveOnDrag(event):
    global curX, processCanvas, processCircle, curVar
    pos = processCanvas.coords(processCircle)
    nextPos = pos[0] + event.x - curX
    if nextPos < 0:
        processCanvas.move(processCircle, -pos[0], 0)
        curX = 0
    elif nextPos > 910:
        processCanvas.move(processCircle, 910-pos[0], 0)
        curX = 910
    else:
        processCanvas.move(processCircle, event.x-curX, 0)
        curX = event.x
    curVar.set(setTime(int(curX/910*audioLength)))

def setTime(length):
    minite = length // 60
    second = length % 60
    str = "{:02d}".format(minite)+":"+"{:02d}".format(second)
    return str

# create framework
mainFrame = tk.Frame(root)
pageFrame = tk.Frame(mainFrame, width=1080, height=570, bg="#FFFFFF", borderwidth=0, highlightthickness=0)
audioFrame = tk.Frame(pageFrame, width=400, height=450, bg="#FFD966", borderwidth=0, highlightthickness=0)
visualFrame = tk.Frame(pageFrame, width=2000, height=450, bg="#F2F2F2", borderwidth=0, highlightthickness=0)
statusFrame = tk.Frame(mainFrame, width=1080, height=50, bg="#BFBFBF", borderwidth=0, highlightthickness=0)
optionFrame = tk.Frame(mainFrame, width=1080, height=100, bg="#A6A6A6", borderwidth=0, highlightthickness=0)

# place framework
mainFrame.pack(fill=tk.BOTH, padx=0, pady=0, expand=True)
mainFrame.pack_propagate(False)
optionFrame.pack(side=tk.BOTTOM, fill=tk.X, padx=0, pady=0)
optionFrame.pack_propagate(False)
statusFrame.pack(side=tk.BOTTOM, fill=tk.X, padx=0, pady=0)
statusFrame.pack_propagate(False)
pageFrame.pack(side=tk.BOTTOM, fill=tk.BOTH, padx=0, pady=0, expand=True)
pageFrame.pack_propagate(False)
audioFrame.pack(side='left', fill=tk.Y, padx=0, pady=0)
audioFrame.pack_propagate(False)
visualFrame.pack(side='right', fill=tk.Y, padx=0, pady=0)
visualFrame.pack_propagate(False)

# create button - optionFrame
modifyCanvas = tk.Canvas(optionFrame, width=150, height=100, bg="#A6A6A6", borderwidth=0, highlightthickness=0)
modifyButton = modifyCanvas.create_image(80, 50, image=modifyImage)
modifyCanvas.tag_bind(modifyButton, "<Button-1>", DISABLED)

optionMidFrame = tk.Frame(optionFrame, bg="#A6A6A6")
startOrPauseCanvas = tk.Canvas(optionMidFrame, width=100, height=100, bg="#A6A6A6", borderwidth=0, highlightthickness=0)
startOrPauseButton = startOrPauseCanvas.create_image(50, 50, image=startImage)
startOrPauseCanvas.tag_bind(startOrPauseButton, "<Button-1>", StartOrPauseChange)

speedVar = ["x 0.5", "x 1.0", "x 2.0"]
speedCombo = ttk.Combobox(optionFrame, width=4, values=speedVar, state="readonly", style="TCombobox")
speedCombo.set("x 1.0")
speedCombo.bind('<<ComboboxSelected>>', on_combobox_select)

replaceCanvas = tk.Canvas(optionFrame, width=150, height=100, bg="#A6A6A6", borderwidth=0, highlightthickness=0)
replaceButton = replaceCanvas.create_image(80, 50, image=replaceImage)
replaceCanvas.tag_bind(replaceButton, "<Button-1>", DISABLED)

# set button - optionFrame
modifyCanvas.pack(side="left", padx=80, pady=5)
optionMidFrame.pack(side="left", pady=0, expand=True, fill=tk.Y)
startOrPauseCanvas.pack(pady=0)
# speedCombo.pack(side="left", padx=0, pady=0)
replaceCanvas.pack(side="right", padx=80, pady=5)

# create scale - statusFrame
curVar = tk.StringVar()
curTime = tk.Label(statusFrame, textvariable=curVar, bg="#BFBFBF", fg="#000000", font=("Arial", 12), width=10, height=20)
endVar = tk.StringVar()
endTime = tk.Label(statusFrame, textvariable=endVar, bg="#BFBFBF", fg="#000000", font=("Arial", 12), width=10, height=20)
curVar.set("00:00")
endVar.set(setTime(audioLength))

processCanvas = tk.Canvas(statusFrame, width=925, borderwidth=0, bg="#BFBFBF", highlightthickness=0)
processLine = processCanvas.create_line(5, 25, 920, 25, width=4)
processCircle = processCanvas.create_oval(0, 20, 10, 30, fill="#C00000")
processCanvas.tag_bind(processCircle, "<Button-1>", moveOnClick)
processCanvas.tag_bind(processCircle, "<B1-Motion>", moveOnDrag)

# set scale - statusFrame
curTime.pack(side="left", padx=0, pady=20)
endTime.pack(side="right", padx=0, pady=20)
processCanvas.pack(pady=0)

# create button - audioFrame
newButton = tk.Button(audioFrame, width=10, height=2, text="Create New", bg="#FFFFFF", fg="#C00000", command=DISABLED)

# set button - audioFrame
newButton.pack(side=tk.TOP, fill=tk.X, padx=20, pady=10)
root.mainloop()