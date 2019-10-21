import tkinter as tk
from tkinter import *
import wx
import os
from PIL import Image, ImageTk
import threading
import multiprocessing
import time
from wxWindows import MainPanelWin,NewPanelWin
import sys

class MainWindow(tk.Frame):
    def __init__(self, x,y,width,height,master=None):
        super().__init__(master)
        self.x = str(x)
        self.y = str(y)
        self.width = str(width)
        self.height = str(height)
        stringthing = "{0}x{1}+{2}+{3}".format(self.width,self.height,self.x,self.y)
        self.images = []  # to hold the newly created image
        self.master = master
        self.pack()
        self.create_widgets()
        self.master.geometry(stringthing)
    def create_widgets(self):
        '''
        self.hi_there = tk.Button(self)
        self.hi_there["text"] = "Hello World\n(click me)"
        self.hi_there["command"] = self.say_hi
        self.hi_there.pack(side="top")

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)                              
        self.quit.pack(side="bottom")
        '''
        self.anothercanvas = Canvas(width=self.width,height=self.height,highlightthickness=5)
        self.anothercanvas.pack()
        self.create_rectangle(self.anothercanvas,0, 0,400,400, fill='white', alpha=0,outline='red',width=0)
        self.master.overrideredirect(True)
        self.master.wait_visibility(self.master)
        self.master.attributes("-alpha", 0.4)
    def quit(self):
        self.master.destroy()
    def create_rectangle(self,canvas,x1, y1, x2, y2, **kwargs):
        if 'alpha' in kwargs:
            alpha = int(kwargs.pop('alpha') * 255)
            fill = kwargs.pop('fill')
            fill = self.master.winfo_rgb(fill) + (alpha,)
            image = Image.new('RGBA', (x2-x1, y2-y1), fill)
            self.images.append(ImageTk.PhotoImage(image))
            canvas.create_image(x1, y1, image=self.images[-1], anchor='nw')
        canvas.create_rectangle(x1, y1, x2, y2, **kwargs)

             
class Application:
    def __init__(self,root_dir,dirs):

        #self.daemon = multiprocessing.Process(target=self.daemon_thread)
        #self.daemon.start()
        self.root_dir = root_dir
        self.dirs = dirs
        self.box = None
        self.name = ""
        self.wxapp = wx.App() 
        self.b = MainPanelWin(None, 'OCR Box',self)
        self.a  = NewPanelWin(None,  'OCR Box',self) 
        self.a.frame = self.b
        self.b.frame = self.a
        self.p2 = multiprocessing.Process(target=self.make_wx_application)
        self.p2.start()
    def daemon_thread(self):
        pass
    def start_tk_thread(self,box,name):
        self.name = name
        self.box = box
        with open(os.path.join(self.dirs["boxes"],name),"w+") as file:
            file.write(" ".join(list(map(str,self.box.values()))))
            file.write(" \n")
        self.p1 = multiprocessing.Process(target=self.make_tk_application)
        self.p1.start()
    def make_tk_application(self):
        if self.box!=None:
            root = tk.Tk()
            x = self.box['x1']
            y = self.box['y1']
            w = int(self.box['x2']) - int(self.box['x1'])
            h = int(self.box['y2'])- int(self.box['y1'])
            self.app = MainWindow(x,y,w,h,master=root)
            self.app.mainloop()
    def make_wx_application(self):    
        self.wxapp.MainLoop()
    def quit(self):
        self.p1.terminate()
        self.a.Destroy()
        self.b.Destroy()
        exit()
    def resize_window(self):
        pass
    def append_region(self,region):    
        with open(os.path.join(self.dirs["boxes"],self.name),"a+") as file:
            file.write(" ".join(list(map(str,region.values()))))
            file.write("\n")
    def append_comp(self):
        pass
    def toggle_visualization_level(self):
        pass
    def quit(self):
        self.p1.terminate()
        exit()

        
class Application_NOGUI:
    def __init__(self,box):
        self.box = box
        self.p1 = multiprocessing.Process(target=self.make_tk_application)
        self.p1.start()
    def make_tk_application(self):
        root = tk.Tk()
        x = self.box['x1']
        y = self.box['y1']
        w = int(self.box['x2']) - int(self.box['x1'])
        h = int(self.box['y2'])- int(self.box['y1'])
        self.app = MainWindow(x,y,w,h,master=root)
        self.app.mainloop()
    