from PIL import Image, ImageTk
import numpy as np
import cv2
import threading
import multiprocessing
import time
import os
import wx
import sys
from screeninfo import get_monitors
from utils import *

class NameDialog(wx.Dialog):
    def __init__(self, parent,monitor,id=-1, title="Confirm Selection"):
        wx.Dialog.__init__(self, parent, id, title, size=(monitor.width//3,monitor.height//2))
        self.parent = parent
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.buttonSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.label = wx.StaticText(self, label=self.parent.Newname)
        self.label2 = wx.StaticText(self, label="Preview:")
        
        self.cancelbutton = wx.Button(self, label="CANCEL",id=2)
        preview = wx.Bitmap("preview.bmp", wx.BITMAP_TYPE_BMP) 
        self.preview = wx.StaticBitmap(self,bitmap=preview,size=(preview.GetWidth(),preview.GetHeight())) 
        self.okbutton = wx.Button(self, label="CONFIRM", id=wx.ID_OK)
        self.mainSizer.Add(self.label, 0, wx.ALL, 8 )
        self.mainSizer.Add(self.label2, 0, wx.ALL, 8 )
        self.mainSizer.Add(self.preview, 0, wx.ALL, 8 )
        self.buttonSizer.Add(self.okbutton, 0, wx.ALL, 8 )
        self.buttonSizer.Add(self.cancelbutton, 0, wx.ALL, 8 )
        self.mainSizer.Add(self.buttonSizer, 0, wx.ALL, 0)

        self.Bind(wx.EVT_BUTTON, self.onOK, id=wx.ID_OK)
        self.Bind(wx.EVT_BUTTON, self.onCancel, id=2)
        self.Bind(wx.EVT_TEXT_ENTER, self.onOK)
        
        self.SetSizer(self.mainSizer)
        self.result = None

    def onOK(self, event):
        self.parent.result = "CONFIRMED"
        self.Hide()
    def onCancel(self, event):
        self.parent.result = "CANCEL"
        self.Hide()
class NewPanelWin(wx.Frame): 
    def __init__(self, parent, title,master): 
        super(NewPanelWin, self).__init__(parent, title = title,size = (600,200))  
        self.Newname = ""
        self.result = None
        self.locations = {}
        self.master =master
        self.root_dir = os.path.dirname(os.path.abspath(__file__))
        self.panel = wx.Panel(self) 

        self.hbox = wx.GridBagSizer(0,0) 
        bmp = wx.Bitmap("new.bmp", wx.BITMAP_TYPE_BMP) 
        self.bmpbtn = wx.BitmapButton(self.panel, id = wx.ID_ANY, bitmap = bmp,
        size = (bmp.GetWidth()-32, bmp.GetHeight()-32)) 
        self.hbox.Add(self.bmpbtn,pos=(0,0),flag=wx.ALL,border=5) 
        self.bmpbtn.Bind(wx.EVT_BUTTON,self.OnClicked) 
        self.bmpbtn.SetLabel("NEW") 
        self.txt = wx.StaticText(self.panel, -1, size=(380,-1))
        self.txt.SetLabel('Press the big plus button to make a new main panel')
        self.hbox.Add(self.txt,pos=(0,1),flag=wx.ALL,border=5)
        self.panel.SetSizer(self.hbox) 
        self.Centre()
        self.Show() 
        self.Bind(wx.EVT_CLOSE,self.OnClose)
    def OnClose(self,event):
       self.frame.Destroy()
       self.Destroy()
    def getBox(self):                
        save_dir = os.path.join(self.root_dir,"temp.pickle")
        self.txt.SetLabel("Please click for the top left corner")            
        get_coordinate(self.Newname,mode="1",save_dir=save_dir)
        self.txt.SetLabel("Please click for the Bottom right corner")            
        get_coordinate(self.Newname,mode="2",save_dir=save_dir)
        locations = pickle_load(save_dir)
        os.remove(save_dir)
        return locations
    def OnClicked(self, event): 
        btn = event.GetEventObject().GetLabel() 
        if(btn=="NEW"):
            dlg = wx.TextEntryDialog(self.panel, 'Whats the name of the main panel?:',"name-o-rama","", 
                    style=wx.OK)
            dlg.ShowModal()
            self.Newname = dlg.GetValue()
            dlg.Destroy()
            if(self.Newname!=""):
                self.locations = self.getBox()
                monitors = get_monitors()
                assert(len(monitors)>0)
                cap = Captuerer(0,0,monitors[0].width,monitors[0].height)
                previewarray = cap.grab().astype(np.uint8)
                previewarray = cv2.rectangle(previewarray,(self.locations['x1'],self.locations['y1']),(self.locations['x2'],self.locations['y2']),(0,255,0),-1)
                previewarray = cv2.resize(previewarray,(int(previewarray.shape[1]//3.3),int(previewarray.shape[0]//3.3)))
                preview = Image.fromarray(previewarray)
                preview.save("preview.bmp")
                self.Hide()
                dlg = NameDialog(self,monitors[0])
                dlg.ShowModal()
                if( self.result == "CANCEL"):
                    self.Show()
                    self.Centre()
                else:
                    self.frame.Newname=self.Newname                    
                    self.master.start_tk_thread(self.locations,self.Newname)
                    self.frame.Show()
    def OnToggle(self,event): 
        state = event.GetEventObject().GetValue() 
        if state == True: 
            print("Toggle button state off")
            event.GetEventObject().SetLabel("click to off") 
        else: 
            print("Toggle button state on")
            event.GetEventObject().SetLabel("click to on")             
class MainPanelWin(wx.Frame): 
    def __init__(self, parent, title,master): 
        super(MainPanelWin, self).__init__(parent, title = title,size = (500,100)) 
        self.Newname= None
        self.master =master
        self.panel = wx.Panel(self) 
        self.vbox = wx.BoxSizer(wx.VERTICAL) 
        self.hbox = wx.GridBagSizer(0,0) 
        bmp = wx.Bitmap("new.bmp", wx.BITMAP_TYPE_BMP) 
        self.bmpbtn = wx.Button(self.panel)
        self.bmpbtn.Bind(wx.EVT_BUTTON,self.OnClicked) 
        self.bmpbtn.SetLabel("NEWREGION") 
        
        bmp1 = wx.Bitmap("new.bmp", wx.BITMAP_TYPE_BMP) 
        self.bmpbtn1 = wx.Button(self.panel)
        self.bmpbtn1.Bind(wx.EVT_BUTTON,self.OnClicked) 
        self.bmpbtn1.SetLabel("NEWCOMP") 
        
        bmp2 = wx.Bitmap("new.bmp", wx.BITMAP_TYPE_BMP) 
        self.bmpbtn2 = wx.Button(self.panel)
        self.bmpbtn2.Bind(wx.EVT_BUTTON,self.OnClicked)
        self.bmpbtn2.SetLabel("SAVE") 
        
        bmp3 = wx.Bitmap("new.bmp", wx.BITMAP_TYPE_BMP) 
        self.bmpbtn3 = wx.Button(self.panel)
        self.bmpbtn3.Bind(wx.EVT_BUTTON,self.OnClicked)
        self.bmpbtn3.SetLabel("QUIT") 

        self.txt = wx.StaticText(self.panel, -1, size=(380,-1))
        self.txt.SetLabel('Info :')

        self.hbox.Add(self.bmpbtn,pos=(0,0),flag=wx.ALL,border=5) 
        self.hbox.Add(self.bmpbtn1,pos=(0,1),flag=wx.ALL,border=5)
        self.hbox.Add(self.bmpbtn2,pos=(0,2),flag=wx.ALL,border=5) 
        self.hbox.Add(self.bmpbtn3,pos=(0,3),flag=wx.ALL,border=5) 
        self.vbox.Add(self.hbox,1,wx.ALIGN_CENTER) 
        self.vbox.Add(self.txt)
        self.panel.SetSizer(self.vbox) 
        self.Bind(wx.EVT_CLOSE,self.OnClose)
    def OnClose(self,event):
        self.master.quit()
    def OnClicked(self, event): 
        btn = event.GetEventObject().GetLabel() 
        print(btn)
        if(btn=="NEWREGION"):
            dlg = wx.TextEntryDialog(self.panel, 'Give it a name',"name-o-rama","", 
                    style=wx.OK)
            dlg.ShowModal()
            if dlg.GetValue()!="":
                self.txt.SetLabel("Please click for the top left corner")            
                region = self.get_ref_box(dlg.GetValue())
                self.master.append_region(region) 
            dlg.Destroy()
        #self.frame.Show()
        #self.Hide()
    def OnToggle(self,event): 
        state = event.GetEventObject().GetValue() 		
        if state == True: 
           print("Toggle button state off")
           event.GetEventObject().SetLabel("click to off") 
        else: 
           print("Toggle button state on")
           event.GetEventObject().SetLabel("click to on") 
    def get_ref_box(self,name):
        '''
            the difference with the reference box is that it
            is written with respect to the proportion to the main box
        '''
        save_dir = os.path.join(self.master.root_dir,"temp.pickle")
        self.txt.SetLabel("Please click for the top left corner WITHIN the selection")
        time.sleep(0.1)
        get_ref_coordinate(name,self.master.box,mode="1",save_dir=save_dir)
        self.txt.SetLabel("Please click for the bottom right corner WITHIN the selection")
        get_ref_coordinate(name,self.master.box,mode="2",save_dir=save_dir)
        ref_locations = pickle_load(save_dir)
        os.remove(save_dir)
        return ref_locations