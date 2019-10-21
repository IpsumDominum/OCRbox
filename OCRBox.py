#Select Scanner version 1.0.0
#Author: Chenrong Lu
#Licsence : MIT liscence 
# How it works:
# First define a scan plane, if not defined, defaults to the whole screen
# Then you can choose to add selections on the plane
# Each selection must be named, otherwise automatically indexed
# A file is used to store all the selections in a pretty straight forward format:
# Just each line:
# name x1 y1 width height
# You can retrieve the OCR results of each box, by 
import os
import time
import pandas as pd
import numpy as np
from utils import *
from WindowMaker import Application
class BoxCreator():
    '''
    'Visual Level': from 1-4, each level is :
                    1: No Image, nothing
                    2: Image is shown but that is it
                    3: Image is shown and boxes are drawn
                    4: Image is shown and boxes are drawn and names are labelled
    'OCR_engine': Currently only supports Tesseract OCR,
                          '''
    def __init__(self,visual_level=4,OCR_engine="tesseract",use_GUI=True):
        self.dirs = {}
        self.root_dir = os.path.dirname(os.path.abspath(__file__))
        for dirs in ['comps','boxes']:
            path = os.path.join(self.root_dir,dirs)
            if(not os.path.isdir(path)):
                os.makedirs(path)
            self.dirs[dirs] = path
        if use_GUI == False:
            while(True):
                choice = prompt("Please select from the following choices",choices=["NewBox|new|n","LoadBox|load|l"]).lower()
                if(choice in["newbox","new","n"]):
                    '''
                        Create a new box
                    '''
                    name = prompt("please give a name to the box")
                    while(name in os.listdir(self.dirs["boxes"])):
                        response = prompt("name already taken, overwrite?",choices=["yes|y","no|n"])
                        if(response in ["yes","y"]):
                            break
                        else:
                            name = prompt("please give a name to the box")
                    self.main_box = self.get_box(name)        
                    print(self.main_box.values())    
                    with open(os.path.join(self.dirs["boxes"],name),"w+") as file:
                        file.write(" ".join(list(map(str,self.main_box.values()))))
                        file.write(" \n")
                    self.name = name
                    break
                elif(choice in["loadbox","load","l"]):
                    '''
                        Load a box
                    '''
                    boxes = os.listdir(self.dirs["boxes"])
                    current_boxes = {choice:item for choice,item in enumerate(boxes)}
                    response = int(prompt("please choose from the list of boxes",current_boxes))
                    while(response not in current_boxes.keys()):
                        response = prompt("INVALID choice, please choose from the list of boxes, or type q to quit",current_boxes)
                        if(response=="q"):
                            exit()
                    self.main_box = self.load_box(current_boxes[response])
                    self.name = self.main_box["name"]
                    break
                else:
                    choice = prompt("Please select from the following choices",choices=["NewBox|new|n","LoadBox|load|l"]).lower()
            self.window = Application_NOGUI(self.main_box)
            while(True):
                choice = prompt("Please select from the following choices",choices=["addOCR","addComp","saveBox","quit|q","print"]).lower()
                if choice=="addocr":
                    self.add_region()
                elif choice =="addcomp":
                    self.add_comp()
                elif choice =="print":
                    with open(os.path.join(self.dirs["boxes"],self.name),'r') as file:
                        print(file.read())
                elif choice =="quit" or choice=="q":
                    self.window.quit()
        else:
            self.window = Application(self.root_dir,self.dirs)
    def load_box(self,box_name):
        box = {}
        with open(os.path.join(self.dirs["boxes"],box_name),'r') as file:
            header = file.readlines()[0].split(" ")
            for i,key in enumerate(["name","x1","y1","x2","y2"]):
                box[key] = header[i]
        return box
    def add_region(self):
        #first prompts for a name
        name = prompt("Please give a name to the region")        
        region = self.get_ref_box(name)
        with open(os.path.join(self.dirs["boxes"],self.name),"a+") as file:
            file.write(" ".join(list(map(str,region.values()))))
            file.write("\n")
    def add_comp(self):
        #first prompts for a name
        name = prompt("Please give a name to the comparison")                        
        #then prepare a directory for comparisons
        #find all the files in the directory which could be compared
        #compare with all files in the directory,
        #Return the name of the file with the most 
    def get_ref_box(self,name):
        '''
            the difference with the reference box is that it
            is written with respect to the proportion to the main box
        '''
        save_dir = os.path.join(self.root_dir,"temp.pickle")
        get_ref_coordinate(name,self.main_box,mode="1",save_dir=save_dir)
        get_ref_coordinate(name,self.main_box,mode="2",save_dir=save_dir)
        ref_locations = pickle_load(save_dir)
        os.remove(save_dir)
        return ref_locations
    def get_box(self,name):
        save_dir = os.path.join(self.root_dir,"temp.pickle")
        get_coodinate(name,mode="1",save_dir=save_dir)
        get_coordinate(name,mode="2",save_dir=save_dir)
        locations = pickle_load(save_dir)
        print(locations)
        os.remove(save_dir)
        return locations
