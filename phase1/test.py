import random
import tkinter as tk
import time
import seaborn as sb
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

root = tk.Tk()
width = root.winfo_width()
height = root.winfo_height()
frame2 = tk.Frame(root)
frame2.pack(fill='both',expand=True)
canvas = None



def cplot(x):
    global canvas
    fig = plt.Figure(figsize = (5, 5), dpi = 100) 
    plot1 = fig.add_subplot(111) 
    y = [i**2 for i in range(x)] 
    print(y)
    plot1.plot(y)
    
    if canvas: canvas.get_tk_widget().pack_forget()  # remove previous image

    canvas = FigureCanvasTkAgg(fig, master=frame2)
    canvas.get_tk_widget().pack()

    canvas.draw()
    for i in range(5):
        print(i+1)
        time.sleep(1)
        
cplot(10)
cplot(100)
root.mainloop() 


# # import all classes/methods 
# # from the tkinter module 
# from tkinter import *
# from matplotlib.figure import Figure 
# from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
# NavigationToolbar2Tk) 

# # plot function is created for 
# # plotting the graph in 
# # tkinter window 
# def plot(): 
#     print("enter plot")
# 	# the figure that will contain the plot 
#     fig = Figure(figsize = (5, 5), dpi = 100) 
#     y = [i**2 for i in range(101)] 
#     plot1 = fig.add_subplot(111) 
#     plot1.plot(y) 
    
#     canvas = FigureCanvasTkAgg(fig, master = window) 
#     canvas.draw() 
#     canvas.get_tk_widget().pack() 
#     print("canvas added")
#     toolbar = NavigationToolbar2Tk(canvas, window) 
#     toolbar.update() 
#     canvas.get_tk_widget().pack() 
#     print('toolbar added')

# # the main Tkinter window 
# window = Tk() 

# # setting the title 
# window.title('Plotting in Tkinter') 

# # dimensions of the main window 
# window.geometry("500x500") 

# # button that displays the plot 
# plot_button = Button(master = window, 
# 					command = plot, 
# 					height = 2, 
# 					width = 10, 
# 					text = "Plot") 

# # place the button 
# # in main window 
# plot_button.pack() 

# # run the gui 
# window.mainloop() 

