import wave
import matplotlib.pyplot as plt
import numpy as np

from functools import partial
import tkinter as tk

import matplotlib
matplotlib.use("TKAgg")
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from recording import Recording

class Visualization():
    def __init__(self, wavFile, frame, interval=100, display_sec =4):
        # wavRecording - Recording object of the audio file
        # frame - tk frame where the visualization graph will be displayed
        self.wavRecording = wavFile
        with wave.open(self.wavRecording.path) as wav:
            self.signal = wav.readframes(-1)
            self.f_rate = wav.getframerate()
        self.pause = False
        self.frame = frame
        self.interval = interval
        self.display_sec = display_sec

    def _secToFrameInd(self, sec):
        return int(sec*self.f_rate/int(self.f_rate*self.interval/1000))

    def visualize(self, offset = 0):
        # offset - (optional) current location in the audio file
        #
        # no return
        # visualization should be displayed in the provided frame
        
        signal = np.frombuffer(self.signal, dtype ="int16")
        time = [i/self.f_rate for i in range(len(signal))]
        
        plt.style.use('fivethirtyeight')
        fig, ax = plt.subplots()
        width = self.frame.winfo_width()
        height = self.frame.winfo_height()
        l = ax.figure.subplotpars.left
        r = ax.figure.subplotpars.right
        t = ax.figure.subplotpars.top
        b = ax.figure.subplotpars.bottom
        figw = float(width)/(r-l)
        figh = float(height)/(t-b)
        ax.figure.set_size_inches(figw, figh)
        plt.plot([-1,2], [0,0])
        
        ## GUI
        canvas = FigureCanvasTkAgg(plt.gcf(), master=self.frame)
        canvas.draw()
        canvas.get_tk_widget().grid(column=0, row=0)
    
        nframes = int(self.f_rate*self.interval/1000)
        length = int(self.display_sec * self.f_rate / nframes)
        print(nframes)
        print(length)
        print(len(signal))
        signal = np.absolute(np.array(signal[0:int(nframes*np.floor(len(signal)/nframes))]))
        time = time[0:int(nframes*np.floor(len(signal)/nframes))]
        mat_sig = np.reshape(signal, (int(np.floor(len(signal)/nframes)), nframes))
        mat_time = np.reshape(np.array(time),(int(np.floor(len(signal)/nframes)), nframes))
        print(mat_sig.shape)
        print(mat_time)
        mat_sig = np.average(mat_sig,axis=1)
        signal = mat_sig.flatten()
        mat_time = mat_time[:,0]
        print(mat_time)
        print(signal.shape)
        time = mat_time.flatten()
        lim_amp = (-np.max(signal),np.max(signal))
        print(time)
        print(len(time))
        ani = FuncAnimation(plt.gcf(), partial(self.animate, time, signal, length, lim_amp, ax), interval=self.interval, frames = range(self._secToFrameInd(offset),len(time)), repeat=False, blit=False)
        # plt.show()
        while self.pause:
            tk.update_idletasks()
            tk.update()

    def stop(self):
        self.pause = True

    def animate(x_vals, y_vals, length, y_lim, ax, i):
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
        ax.grid()


# root = tk.Tk()
# mainFrame = tk.Frame(root)
# wavRecording = Recording('list1', '','','','./audioFile/harvard_list1.wav')
# vis = Visualization(wavRecording, mainFrame)
# vis.visualize(12)