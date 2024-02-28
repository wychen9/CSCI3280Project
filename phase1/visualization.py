import wave
import matplotlib.pyplot as plt
import numpy as np
import time

from functools import partial
import tkinter as tk

import matplotlib
matplotlib.use("TKAgg")
from matplotlib import pyplot as plt

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from recording import Recording
from matplotlib.animation import FuncAnimation 

class Visualization():
    def __init__(self, wavFile, frame, interval=50, display_sec =4):
        # wavRecording - Recording object of the audio file
        # frame - tk frame where the visualization graph will be displayed
        self.wavRecording = wavFile
        with wave.open(self.wavRecording.path) as wav:
            self.signal = wav.readframes(-1)
            self.f_rate = wav.getframerate()
        self.start = False
        self.pause = False
        self.frame = frame
        self.interval = interval
        self.display_sec = display_sec
        self.nframes = int(self.f_rate*self.interval/1000)
        self.length = int(self.display_sec * self.f_rate / self.nframes)
        # print("nframes: " + str(self.nframes))
        # print("length: " + str(self.length))
        self.signal = np.frombuffer(self.signal, dtype ="int16")
        self.time = [i/self.f_rate for i in range(len(self.signal))]
        self.fig, self.ax=plt.subplots()
        self._initFig()
        self._processData()
        self.signal_lim = (-np.max(self.signal),np.max(self.signal))
        self.canvas = None
        # self._bindCanvas()
    def _secToFrameInd(self, sec):
        ret = int(sec*self.f_rate/int(self.f_rate*self.interval/1000))
        # print("return value: " + str(ret))
        return ret

    def _processData(self):
        signal = self.signal
        time = self.time

        signal = np.absolute(np.array(signal[0:int(self.nframes*np.floor(len(signal)/self.nframes))]))
        time = time[0:int(self.nframes*np.floor(len(signal)/self.nframes))]
        
        mat_sig = np.reshape(signal, (int(np.floor(len(signal)/self.nframes)), self.nframes))
        mat_time = np.reshape(np.array(time),(int(np.floor(len(signal)/self.nframes)), self.nframes))
        mat_sig = np.average(mat_sig,axis=1)
        mat_time = mat_time[:,0]
        
        self.signal = mat_sig.flatten()
        self.time = mat_time.flatten()

    def _initFig(self):
        plt.style.use('fivethirtyeight')
        plt.ion()
        # width = 5
        # height = 3
        width = self.frame.winfo_width()
        height = self.frame.winfo_height()
        # fig, ax = plt.subplots()

        l = self.ax.figure.subplotpars.left
        r = self.ax.figure.subplotpars.right
        t = self.ax.figure.subplotpars.top
        b = self.ax.figure.subplotpars.bottom
        self.ax.figure.set_size_inches(float(width)/(r-l), float(height)/(t-b))
        # return fig, self.ax

    def begin(self, offset=0, endPoint=-1):
        # offset - (optional) current location in the audio file, 0 by default
        # endPoint - (optional) end location of visualization, -1 by default
        #
        # no return
        # animated visualization should be displayed in the provided frame
        
        # print("endPoint: " + str(endPoint))
        endInd = self._secToFrameInd(endPoint)
        # print("endInd: " + str(endInd))
        if(endPoint<0 or endInd>= len(self.time)):
            endInd = len(self.time)-1
        
        # print("time length: " + str(len(self.time)))
        # print("start point: " + str(self._secToFrameInd(offset)))
        # print("end point: " + str(endInd))

        if self.canvas: self.canvas.get_tk_widget().pack_forget()  # remove previous image
    
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas.get_tk_widget().pack(expand=True, fill='both')

        ani = FuncAnimation(self.fig, partial(self.animate, self.time, self.signal, self.length, self.signal_lim, self.ax), 
                                                 frames=range(self._secToFrameInd(offset),endInd), 
                                                 interval=self.interval-10, 
                                                 repeat = False,
                                                 blit=False)
        
        self.canvas.draw()
        self.locAt(endInd-1)
        

    def locAt(self, offset=-1):
        # offset - (optional) current location in the audio file
        #
        # no return
        # static visualization should be displayed in the provided frame

        print("receive " + str(offset))
        if(offset<0 or offset>len(self.time)):
            offset = len(self.time) - 1
        print("location at " + str(offset))

        if self.canvas: self.canvas.get_tk_widget().pack_forget()  # remove previous image
    
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas.get_tk_widget().pack(expand=True, fill='both')

        self.animate(self.time, self.signal, self.length, self.signal_lim, self.ax, offset)
        self.canvas.draw()

    def animate(self,x_vals, y_vals, length, y_lim, ax, i):
        ax.cla()
        start = int(np.floor(i - length/2))
        stop =  int(np.ceil(i + length/2))
        if(stop<len(x_vals) and start >= 0): 
            plt.vlines(x_vals[start:stop],-y_vals[start:stop], y_vals[start:stop],linewidth = 1)
            ax.set(xlim = (x_vals[start],x_vals[stop]), ylim =y_lim)
        elif(stop>= len(x_vals)):
            plt.vlines(x_vals[start:-1],-y_vals[start:-1], y_vals[start:-1],linewidth = 1)
            diff = x_vals[i] - x_vals[i-1]
            cnt = stop-len(x_vals)
            plt.hlines(0, x_vals[-1], x_vals[-1]+diff*cnt, alpha=0.2, linewidth =1)
            ax.set(xlim = (x_vals[start],x_vals[-1]+(cnt-1)*diff), ylim =y_lim)
        else:
            plt.vlines(x_vals[0:stop],-y_vals[0:stop],y_vals[0:stop], linewidth = 1)
            diff = x_vals[i] - x_vals[i+1]
            cnt = int(np.floor(np.absolute(start)))
            plt.hlines(0, x_vals[0]+cnt*diff, x_vals[0], alpha=0.2,linewidth =1)
            ax.set(xlim = (x_vals[0]+(cnt-1)*diff,x_vals[stop]), ylim =y_lim)
        plt.vlines(x_vals[i], y_lim[0], y_lim[1], colors='r', linewidth = 2) 
        ax.set_axis_off()

## sample usages
# root = tk.Tk()
# root.geometry("500x300")
# width = root.winfo_width()
# height = root.winfo_height()
# frame2 = tk.Frame(root,bg='black', width=width, height=height)
# frame2.pack(fill='both', expand=True)

# wavRecording = Recording('list1', '','','','./audioFile/harvard_list1.wav')
# vis = Visualization(wavRecording, frame2)
# vis.begin(22,25)
# root.mainloop()