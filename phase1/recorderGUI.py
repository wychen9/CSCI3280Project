# Install:
#   python3 -m pip install SpeechRecognition
#   brew install flac (for mac), 

import audioTrim
import recording
import audioRecorder
import enhancements.speech2text as st
import datetime
import tkinter as tk
from tkinter import PhotoImage

recorder = audioRecorder.AudioRecorder()
index = 0
click = 0
click_modify = 0
click_replace = 0
isPlaying = False
isReplacing = False
isRecording = False
tmpLength = 0

# curRecording = recording.Recording()
curRecording = recording.Recording()
audioLength = curRecording.length
curLabel = curRecording.label

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

def recordNew():
    if isRecording:
        endVar.set(setTime(setNumber(endVar.get())+1))
        processCanvas.after(1000, recordNew)
    return

def move():
    global isPlaying, click, curVar, tmpLength
    if processCanvas.coords(processCircle)[0] <= 910 and (isPlaying or isReplacing):
        processCanvas.move(processCircle, float(910/(audioLength*10))*float(speedVar.get()), 0)
        curVar.set(setTime(int(processCanvas.coords(processCircle)[0]/910*audioLength)))
        tmpLength = processCanvas.coords(processCircle)[0]
        processCanvas.after(100, move)
    elif processCanvas.coords(processCircle)[0] > 910:
        if isReplacing:
            tmp = int(tmpLength/910*audioLength)
            curVar.set(setTime(tmp))
            endVar.set(setTime(tmp))
            tmpLength += float(910/(audioLength*10)*float(speedVar.get()))
            processCanvas.after(100, move)
        else:
            click += 1
            startOrPauseCanvas.itemconfig(startOrPauseButton, image=startImage)
            isPlaying = False

def StartOrPauseChange(event):
    global click, isPlaying, isRecording, audioLength
    if click % 2 == 0:
        if processCanvas.coords(processCircle)[0] > 910:
            processCanvas.coords(processCircle, 0, 20, 10, 30)
        startOrPauseCanvas.itemconfig(startOrPauseButton, image=pauseImage)
        isPlaying = True
        if audioLength > 0:
            processCanvas.after(0, move)
        else:
            isRecording = True
            recorder.start_recording()
            processCanvas.after(0, recordNew)
    else:
        startOrPauseCanvas.itemconfig(startOrPauseButton, image=startImage)
        isPlaying = False
        if isRecording:
            # ----function----
            curRecording.length = recorder.get_total_recording_length()
            curRecording.path = recorder.stop_recording()
            print(recorder.get_total_recording_length())
            audioLength = curRecording.length
            # ----function----
            isRecording = False
    click += 1

def ModifyOrEnsureChange(event):
    global click_modify, processCircle, curVar, endVar, audioLength, isModifying, tagVar
    if click_modify % 2 == 0:
        print("modify")
        modifyCanvas.itemconfig(modifyButton, image=ensureImage)
        modify()
    else:
        # ----function----
        audioTrim(setNumber(curVar.get()), setNumber(endVar.get()), curRecording)
        # ----function----
        modifyCanvas.itemconfig(modifyButton, image=modifyImage)
        curRecording.length = setNumber(endVar.get()) - setNumber(curVar.get())
        curRecording.createTime = datetime.datetime.now()
        tmpStr = "   "+ curRecording.name + "\n\n   " + curRecording.createTime.strftime("%Y-%m-%d %H:%M:%S")+"            " + \
                        setTime(curRecording.length)
        tagVar.set(tmpStr)
        curVar.set(setTime(0))
        # audioLength = int((processCanvas.coords(endCircle)[0]-processCanvas.coords(startCircle)[0])/910*audioLength)
        audioLength = curRecording.length
        endVar.set(setTime(audioLength))
        processCanvas.delete(startCircle)
        processCanvas.delete(endCircle)
        processCircle = processCanvas.create_oval(0, 20, 10, 30, fill="#C00000")
        processCanvas.tag_bind(processCircle, "<Button-1>", lambda event, circle=processCircle: moveOnClick(event, circle))
        processCanvas.tag_bind(processCircle, "<B1-Motion>", lambda event, circle=processCircle, var=curVar: moveOnDrag(event, circle, var))
    click_modify += 1

def ReplaceOrEnsureChange(event):
    global click_replace, isReplacing, curVar, audioLength, isPlaying, click, tmpLength, replaceStart
    if click_replace % 2 == 0:
        replaceCanvas.itemconfig(replaceButton, image=ensureImage)
        speedVar.set("1.0")
        isReplacing = True
        replaceStart = setNumber(curVar.get())
        recorder.start_recording()
        replace()
    else:
        # ----function----
        tmpPath = recorder.stop_recording()
        tempRecording = recording("tmp", datetime.datetime.now(), setNumber(curVar.get())-replaceStart, None, tmpPath)
        audioTrim.overwrite(replaceStart, setNumber(curVar.get()), curRecording, tempRecording)
        # ----function----
        isReplacing = False
        if tmpLength > 910:
            audioLength = int(audioLength + (tmpLength - 910)/910*audioLength)
        replaceCanvas.itemconfig(replaceButton, image=replaceImage)
        processCanvas.delete(replaceCircle)
        tmpLength = 0
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

def setNumber(str):
    return 60*int(str[:2])+int(str[3:])
 
def labelOnClick(event):
    global curVar, endVar, audioLength, processCanvas, processCircle, curLabel
    for i in recordingsList:
        i.label.config(bg="#E3B00B")
    event.widget.config(bg="#FFE699")
    print(labelTag[event.widget])
    curRecording = recordingsList[labelTag[event.widget]]
    audioLength = curRecording.length
    curLabel = curRecording.label
    endVar.set(setTime(recordingsList[labelTag[event.widget]].length))
    curVar.set(setTime(0))
    processCanvas.coords(processCircle, 0, 20, 10, 30)
    textVar.set(st.speech2text(curRecording.path))

def createNew():
    global index, allFrame, recordingCanvas, curRecording, audioLength, curLabel, tagVar
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
    curVar.set(setTime(0))
    endVar.set(setTime(0))
    curRecording = record
    audioLength = record.length
    curLabel = newLabel

    recordingCanvas.update_idletasks() 
    recordingCanvas.config(scrollregion=recordingCanvas.bbox("all"))
    index += 1

def text():
    if tInt.get() == 1:
        print("changing to text")
        textVar.set(st.speech2text(curRecording.path))
    else:
        textVar.set("Hello! Welcome to Our Recorder :)")
    textCanvas.update_idletasks() 
    textCanvas.config(scrollregion=textCanvas.bbox("all"))

def visual():
    return

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
chooseFrame = tk.Frame(visualFrame, width=700, height=20, bg="#F2F2F2", borderwidth=0, highlightthickness=0)
contentFrame = tk.Frame(visualFrame, width=700, height=400, bg="#F2F2F2", borderwidth=0, highlightthickness=0)
visualFrame = tk.Frame(contentFrame, width=700, height=300, bg="white", borderwidth=0, highlightthickness=0)
textFrame = tk.Frame(contentFrame, width=700, height=300, bg="white", borderwidth=0, highlightthickness=0)
textScorll = tk.Scrollbar(textFrame)
textCanvas = tk.Canvas(textFrame, width=700, height=1000, bg="white", borderwidth=0, highlightthickness=0, yscrollcommand=textScorll.set)
textVar = tk.StringVar()
textLabel = tk.Label(textCanvas, bg="white", textvariable=textVar, wraplength=500, borderwidth=0, highlightthickness=0, \
                     anchor="nw", justify=tk.LEFT)
textScorll.config(command=textCanvas.yview)
textWindow = textCanvas.create_window(0, 0, anchor='nw', window=textLabel)
textVar.set("Hello! Welcome to Our Recorder :)")

textCanvas.update_idletasks() 
textCanvas.config(scrollregion=textCanvas.bbox("all"))

tvFrame = tk.Frame(chooseFrame, width=200, height=20, bg="#F2F2F2", borderwidth=0, highlightthickness=0)
tInt = tk.IntVar()
vInt = tk.IntVar()
tButton = tk.Checkbutton(tvFrame, text="Text", variable=tInt, bg="#F2F2F2", command=text)
vButton = tk.Checkbutton(tvFrame, text="Image", variable=vInt, bg="#F2F2F2", command=DISABLED)

speedFrame = tk.Frame(chooseFrame, width=300, height=20, bg="#F2F2F2", borderwidth=0, highlightthickness=0)
speedVar = tk.StringVar()
slowR = tk.Radiobutton(speedFrame, text="x 0.5", variable=speedVar, value="0.5", bg="#F2F2F2")
normalR = tk.Radiobutton(speedFrame, text="x 1.0", variable=speedVar, value="1.0", bg="#F2F2F2")
fastR = tk.Radiobutton(speedFrame, text="x 2.0", variable=speedVar, value="2.0", bg="#F2F2F2")
speedVar.set("1.0")

# set button - visualFrame
chooseFrame.pack(side=tk.TOP, fill=tk.X)
contentFrame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
speedFrame.pack(side=tk.LEFT, fill=tk.Y)
tvFrame.pack(side=tk.RIGHT, fill=tk.Y)
tButton.pack(side=tk.LEFT, padx=5)
vButton.pack(side=tk.LEFT, padx=5)
fastR.pack(side=tk.RIGHT, padx=5)
normalR.pack(side=tk.RIGHT, padx=5)
slowR.pack(side=tk.RIGHT, padx=5)
visualFrame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
textFrame.pack(side=tk.TOP, fill=tk.BOTH, padx=5, pady=5)
textScorll.pack(side=tk.RIGHT, fill=tk.Y)
textCanvas.pack(side=tk.LEFT, fill=tk.BOTH)
root.mainloop()