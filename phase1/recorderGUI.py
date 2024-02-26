import recording
import datetime
import tkinter as tk
from tkinter import PhotoImage

index = 0
click = 0
click_modify = 0
click_replace = 0
isPlaying = False
isReplacing = False
audioLength = 100
tmpLength = 0

labelTag = {}
recordingsList = []

root = tk.Tk()
root.title("Video Recorder")
root.geometry("1080x720")
root.resizable(width=False, height=False)

# import images
modifyImage = PhotoImage(file="images/Modify.PNG")
startImage = PhotoImage(file="images/Start.PNG")
pauseImage = PhotoImage(file="images/Pause.PNG")
replaceImage = PhotoImage(file="images/Replace.PNG")
ensureImage = PhotoImage(file="images/Ensure.PNG")
# define functions

def DISABLED(event):
    print("click")
    return 

def move():
    global isPlaying, click, curVar, tmpLength
    if processCanvas.coords(processCircle)[0] <= 910 and (isPlaying or isReplacing):
        processCanvas.move(processCircle, float(910/(audioLength*10)), 0)
        curVar.set(setTime(int(processCanvas.coords(processCircle)[0]/910*audioLength)))
        tmpLength = processCanvas.coords(processCircle)[0]
        processCanvas.after(100, move)
    elif processCanvas.coords(processCircle)[0] > 910:
        if isReplacing:
            tmp = int(tmpLength/910*audioLength)
            curVar.set(setTime(tmp))
            endVar.set(setTime(tmp))
            tmpLength += float(910/(audioLength*10))
            processCanvas.after(100, move)
        else:
            click += 1
            startOrPauseCanvas.itemconfig(startOrPauseButton, image=startImage)
            isPlaying = False

def StartOrPauseChange(event):
    global click, isPlaying
    if click % 2 == 0:
        if processCanvas.coords(processCircle)[0] > 910:
            processCanvas.coords(processCircle, 0, 20, 10, 30)
        startOrPauseCanvas.itemconfig(startOrPauseButton, image=pauseImage)
        isPlaying = True
        processCanvas.after(0, move)
    else:
        startOrPauseCanvas.itemconfig(startOrPauseButton, image=startImage)
        isPlaying = False
    click += 1

def ModifyOrEnsureChange(event):
    global click_modify, processCircle, curVar, endVar, audioLength, isModifying
    if click_modify % 2 == 0:
        modifyCanvas.itemconfig(modifyButton, image=ensureImage)
        modify()
    else:
        modifyCanvas.itemconfig(modifyButton, image=modifyImage)
        curVar.set(setTime(0))
        audioLength = int((processCanvas.coords(endCircle)[0]-processCanvas.coords(startCircle)[0])/910*audioLength)
        endVar.set(setTime(audioLength))
        processCanvas.delete(startCircle)
        processCanvas.delete(endCircle)
        processCircle = processCanvas.create_oval(0, 20, 10, 30, fill="#C00000")
        processCanvas.tag_bind(processCircle, "<Button-1>", lambda event, circle=processCircle: moveOnClick(event, circle))
        processCanvas.tag_bind(processCircle, "<B1-Motion>", lambda event, circle=processCircle, var=curVar: moveOnDrag(event, circle, var))
    click_modify += 1

def ReplaceOrEnsureChange(event):
    global click_replace, isReplacing, curVar, audioLength, isPlaying, click
    if click_replace % 2 == 0:
        replaceCanvas.itemconfig(replaceButton, image=ensureImage)
        if isPlaying:
            startOrPauseCanvas.itemconfig(startOrPauseButton, image=startImage)
            isPlaying = False
            click += 1
        isReplacing = True
        replace()
    else:
        isReplacing = False
        audioLength = int(tmpLength/910*audioLength)
        replaceCanvas.itemconfig(modifyButton, image=replaceImage)
        processCanvas.delete(replaceCircle)
    click_replace += 1

def modify():
    global curVar, endVar, startCircle, endCircle
    curVar.set(setTime(0))
    processCanvas.delete(processCircle)
    startCircle = processCanvas.create_oval(0, 20, 10, 30, fill="#C00000")
    endCircle = processCanvas.create_oval(910, 20, 920, 30, fill="#C00000")
    processCanvas.tag_bind(startCircle, "<Button-1>", lambda event, circle=startCircle : moveOnClick(event, circle))
    processCanvas.tag_bind(startCircle, "<B1-Motion>", lambda event, circle=startCircle, var=curVar: moveOnDrag(event, circle, var))
    processCanvas.tag_bind(endCircle, "<Button-1>", lambda event, circle=endCircle : moveOnClick(event, circle))
    processCanvas.tag_bind(endCircle, "<B1-Motion>", lambda event, circle=endCircle, var=endVar: moveOnDrag(event, circle, var))

def replace():
    global replaceCircle
    x1, y1, x2, y2 = processCanvas.coords(processCircle)
    replaceCircle = processCanvas.create_oval(x1, y1, x2, y2, fill="#C00000")
    processCanvas.after(0, move)
    return

def moveOnClick(event, circle):
    global curX
    processCanvas.tag_raise(circle)
    curX = event.x 

def moveOnDrag(event, circle, var):
    global curX
    pos = processCanvas.coords(circle)
    nextPos = pos[0] + event.x - curX
    if nextPos < 0:
        processCanvas.move(circle, -pos[0], 0)
        curX = 0
    elif nextPos > 910:
        processCanvas.move(circle, 910-pos[0], 0)
        curX = 910
    else:
        processCanvas.move(circle, event.x-curX, 0)
        curX = event.x
    var.set(setTime(int(curX/910*audioLength)))

def setTime(length):
    minite = length // 60
    second = length % 60
    str = "{:02d}".format(minite)+":"+"{:02d}".format(second)
    return str

def labelOnClick(event):
    global curVar, endVar, audioLength, processCanvas, processCircle
    for i in recordingsList:
        i.label.config(bg="#E3B00B")
    event.widget.config(bg="#FFE699")
    print(labelTag[event.widget])
    audioLength = recordingsList[labelTag[event.widget]].length
    endVar.set(setTime(recordingsList[labelTag[event.widget]].length))
    curVar.set(setTime(0))
    processCanvas.coords(processCircle, 0, 20, 10, 30)

def createNew():
    global index, allFrame, recordingCanvas
    tagVar = tk.StringVar()
    newLabel = tk.Label(allFrame, textvariable=tagVar, width=40, height=5, bg="#FFE699", \
                        anchor="w", justify=tk.LEFT)
    record = recording.Recording("New Recording "+str(index), datetime.datetime.now(), 0, newLabel, None)
    tmpStr = "   "+ record.name + "\n\n   " + record.createTime.strftime("%Y-%m-%d %H:%M:%S")+"            " + \
                        setTime(record.length)
    tagVar.set(tmpStr)
    newLabel.pack(side=tk.BOTTOM, padx=0, pady=3)
    newLabel.bind("<Button-1>", labelOnClick)
    if len(recordingsList) >= 1:
        for i in recordingsList:
            i.label.config(bg="#E3B00B")
    recordingsList.append(record)
    labelTag[newLabel] = index
    recordingCanvas.update_idletasks() 
    recordingCanvas.config(scrollregion=recordingCanvas.bbox("all"))
    index += 1

# create framework
mainFrame = tk.Frame(root)
pageFrame = tk.Frame(mainFrame, width=1080, height=570, bg="#FFFFFF", borderwidth=0, highlightthickness=0)
audioFrame = tk.Frame(pageFrame, width=300, height=450, bg="#FFD966", borderwidth=0, highlightthickness=0)
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
modifyCanvas.tag_bind(modifyButton, "<Button-1>", ModifyOrEnsureChange)

optionMidFrame = tk.Frame(optionFrame, bg="#A6A6A6")
startOrPauseCanvas = tk.Canvas(optionMidFrame, width=100, height=100, bg="#A6A6A6", borderwidth=0, highlightthickness=0)
startOrPauseButton = startOrPauseCanvas.create_image(50, 50, image=startImage)
startOrPauseCanvas.tag_bind(startOrPauseButton, "<Button-1>", StartOrPauseChange)

replaceCanvas = tk.Canvas(optionFrame, width=150, height=100, bg="#A6A6A6", borderwidth=0, highlightthickness=0)
replaceButton = replaceCanvas.create_image(80, 50, image=replaceImage)
replaceCanvas.tag_bind(replaceButton, "<Button-1>", ReplaceOrEnsureChange)

# set button - optionFrame
modifyCanvas.pack(side="left", padx=80, pady=5)
optionMidFrame.pack(side="left", pady=0, expand=True, fill=tk.Y)
startOrPauseCanvas.pack(pady=0)
replaceCanvas.pack(side="right", padx=80, pady=5)

# create scale - statusFrame
curVar = tk.StringVar()
curTime = tk.Label(statusFrame, textvariable=curVar, bg="#BFBFBF", fg="#000000", font=("Arial", 12), width=10, height=20)
endVar = tk.StringVar()
endTime = tk.Label(statusFrame, textvariable=endVar, bg="#BFBFBF", fg="#000000", font=("Arial", 12), width=10, height=20)
curVar.set("00:00")
endVar.set(setTime(audioLength))

processCanvas = tk.Canvas(statusFrame, width=925, borderwidth=0, bg="#BFBFBF", highlightthickness=0) 
processLine = processCanvas.create_line(5, 25, 915, 25, width=4)
processCircle = processCanvas.create_oval(0, 20, 10, 30, fill="#C00000")
processCanvas.tag_bind(processCircle, "<Button-1>", lambda event, circle=processCircle: moveOnClick(event, circle))
processCanvas.tag_bind(processCircle, "<B1-Motion>", lambda event, circle=processCircle, var=curVar: moveOnDrag(event, circle, var))

# set scale - statusFrame
curTime.pack(side="left", padx=0, pady=20)
endTime.pack(side="right", padx=0, pady=20)
processCanvas.pack(pady=0)

# create scorll bar - audioFrame
newButton = tk.Button(audioFrame, width=10, height=2, text="Create New", bg="#FFFFFF", fg="#C00000", command=createNew)
recordingFrame = tk.Frame(audioFrame, width=250, height=600, bg="#FFD966")
recordingCanvas = tk.Canvas(recordingFrame, width=250, height=800, bg="#FFD966", borderwidth=0, highlightthickness=0)
recordingScorll = tk.Scrollbar(recordingFrame, orient="vertical", command=recordingCanvas.yview)
scorlledFrame = tk.Frame(recordingCanvas, width=250, height=600, bg="#FFD966")
recordingCanvas.create_window((0, 0), window=scorlledFrame, anchor="nw")
recordingCanvas.configure(yscrollcommand=recordingScorll.set)
allFrame = scorlledFrame

# set button - audioFrame
newButton.pack(side=tk.TOP, fill=tk.X, padx=20, pady=10)
recordingFrame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=20, pady=10)
recordingCanvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
recordingScorll.pack(side=tk.RIGHT, fill=tk.Y)

# create button - visualFrame
chooseFrame = tk.Frame(visualFrame, width=500, height=20, bg="#F2F2F2", borderwidth=0, highlightthickness=0)
contentFrame = tk.Frame(chooseFrame, width=200, height=20, bg="#F2F2F2", borderwidth=0, highlightthickness=0)
visualVar = tk.StringVar()
textR = tk.Radiobutton(contentFrame, text="Text", variable=visualVar, value="Text", bg="#F2F2F2")
imageR = tk.Radiobutton(contentFrame, text="Image", variable=visualVar, value="Image", bg="#F2F2F2")
visualVar.set("Image")

speedFrame = tk.Frame(chooseFrame, width=300, height=20, bg="#F2F2F2", borderwidth=0, highlightthickness=0)
speedVar = tk.StringVar()
slowR = tk.Radiobutton(speedFrame, text="x 0.5", variable=speedVar, value="0.5", bg="#F2F2F2")
normalR = tk.Radiobutton(speedFrame, text="x 1.0", variable=speedVar, value="1.0", bg="#F2F2F2")
fastR = tk.Radiobutton(speedFrame, text="x 2.0", variable=speedVar, value="2.0", bg="#F2F2F2")
speedVar.set("1.0")

# set button - visualFrame
chooseFrame.pack(side=tk.TOP, fill=tk.X)
contentFrame.pack(side=tk.RIGHT, fill=tk.Y)
speedFrame.pack(side=tk.LEFT, fill=tk.Y)
fastR.pack(side=tk.RIGHT, padx=5)
normalR.pack(side=tk.RIGHT, padx=5)
slowR.pack(side=tk.RIGHT, padx=5)
imageR.pack(side=tk.RIGHT, padx=5)
textR.pack(side=tk.RIGHT, padx=5)

root.mainloop()