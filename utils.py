from pynput.mouse import Listener
import time
import pickle
import cv2
import mss
import numpy as np
class Captuerer:
    def __init__(self,top,left,width,height):
        self.spec = {"top": top, "left": left, "width": width, "height": height}
        title = "capture"
        self.sct = mss.mss()
    def grab(self):
        img = np.asarray(self.sct.grab(self.spec))
        return img
    def close(self):
        self.sct.close()
#a tool to set corners to which the window is to be detected
#first query left top corner 
#then query bottom right corner
def prompt(message,choices=None):
    print(message)
    if(choices!=None):
        print(choices)
    print(">",end="")
    return input()
def get_coordinate(name,mode="1",save_dir="locations.npy"):
    if mode=="1":
        print("Please select top left corner")
    elif mode=="2":
        print("Please select bottom right corner")
    else:
        raise Exception("only valid modes are : 1 2, you have selected {0}".format(mode))
    def on_move(x,y):
        pass
    def on_click(x,y,button,pressed):
        print("\033c")
        listener.stop()
        try:
            locations = pickle_load(save_dir)
            if(mode=="1"):
                locations["x1"] = x
                locations["y1"] = y
            elif(mode=="2"):
                locations["x2"] = x
                locations["y2"] = y
            pickle_save(save_dir,locations)
        except FileNotFoundError:
            locations = {}
            locations['name'] = name
            if(mode=="1"):
                locations["x1"] = x
                locations["y1"] = y
            elif(mode=="2"):
                locations["x2"] = x
                locations["y2"] = y
            pickle_save(save_dir,locations)
        print("success")
        time.sleep(0.3)
    with Listener(on_move=on_move,on_click=on_click) as listener:
        listener.join()
def get_ref_coordinate(name,ref,mode="1",save_dir="locations.npy"):
    if mode=="1":
        print("Please select top left corner")
    elif mode=="2":
        print("Please select bottom right corner")
    else:
        raise Exception("only valid modes are : 1 2, you have selected {0}".format(mode))
    def on_move(x,y):
        pass
    def on_click(x,y,button,pressed):
        print("\033c")
        
        '''
            first check if selection is in the box
        '''
        for key in ['x1','y1','x2','y2']:
            ref[key]= int(ref[key])
        if (x>ref['x1'] and x<ref['x2'] and y>ref['y1'] and y<ref['y2']):
            listener.stop()
            try:
                locations =  pickle_load(save_dir)
                if(mode=="1"):
                    locations["x1"] = int((x - ref['x1']) / (ref['x2']-ref['x1']))
                    locations["y1"] = int((x - ref['y1']) / (ref['y2']-ref['y1']))
                elif(mode=="2"):
                    locations["x2"] = int((x - ref['x1']) / (ref['x2']-ref['x1']))
                    locations["y2"] = int((x - ref['y1']) / (ref['y2']-ref['y1']))
                pickle_save(save_dir,locations)
            except FileNotFoundError:
                locations = {}
                locations['name'] = name
                if(mode=="1"):
                    locations["x1"] = int((x - ref['x1']) / (ref['x2']-ref['x1']))
                    locations["y1"] = int((x - ref['y1']) / (ref['y2']-ref['y1']))
                elif(mode=="2"):
                    locations["x2"] = int((x - ref['x1']) / (ref['x2']-ref['x1']))
                    locations["y2"] = int((x - ref['y1']) / (ref['y2']-ref['y1']))
                pickle_save(save_dir,locations)
            print("success")
            time.sleep(0.3)
        else:
            print("Please Click within the selected reference box!")
    with Listener(on_move=on_move,on_click=on_click) as listener:
        listener.join()
def get_mouse_loc(basex,basey,width,height):
    print(basex,basey)
    def on_move(x,y):
        pass
    def on_click(x,y,button,pressed):
        if(x>basex and y>basey):
            print((x-basex)/width,(y-basey)/height)
    def on_scroll(x,y,dx,dy):
        listener.stop()
    with Listener(on_scroll=on_scroll,on_move=on_move,on_click=on_click) as listener:
        listener.join()
def pickle_save(directory,item):
    with open(directory,'wb') as file:
        pickle.dump(item,file)
def pickle_load(directory):
    with open(directory,'rb') as file:
        item = pickle.load(file)
        print(item)
        return item

