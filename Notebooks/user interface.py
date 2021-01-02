# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 12:03:31 2020

@author: Muhammad Ahmed
"""

import tkinter as Tk
import tkinter.font as tkFont
from tkinter import ttk,Canvas
from tkinter import filedialog
from tkinter import PhotoImage
from functions import getFrames,apply_mask
import cv2 as cv
import numpy as np
from PIL import ImageTk, Image
import subprocess
from time import perf_counter
from math import ceil

def detect_object():
    #making global objects to save the result
    global frames,FILENAME,total_frames
    FILENAME = filedialog.askopenfilename(title='Choose a file')
    fontStyle = tkFont.Font(family="Lucida Grande", size=20)
    images=[]
    duration_frames=0
    #loading video
    VideoCap = cv.VideoCapture(FILENAME)
    hasFrames,image = VideoCap.read()
    #starting timer
    start=perf_counter()
    #counting total number of frames
    while hasFrames:
        hasFrames,image = VideoCap.read()
        duration_frames+=1
    end=perf_counter()
    total_frames=duration_frames
    #loading same video again
    VideoCap1 = cv.VideoCapture(FILENAME)
    hasFrames,image = VideoCap1.read()
    images.append(image)
    total=0
    #saving frames
    while hasFrames:
        hasFrames,image = VideoCap1.read()
        if hasFrames:
            total+=1
            images.append(image)
            if total%30==0:
                output_text='Frames Fetched '+str(ceil(total*100/total_frames))+'%'
                label=Tk.Label(window, text=output_text,font=fontStyle).place(x=5,y=450)#
                window.update()
    frames=images
            
def calculate_first_mask(frames,skip=30):
    #this function calculates mask for very first frame
    frame1=frames[0]
    gray1 = cv.cvtColor(frame1, cv.COLOR_BGR2GRAY)
    gray1 = cv.GaussianBlur(gray1, (3, 3), 0)
    length,width,color=frames[0].shape
    mask=np.zeros((length,width),dtype=np.uint8)
    dimension=frame1.shape[0]*frame1.shape[1]
    #
    for i in range(1,skip):
        frame2=frames[i]
        gray2 = cv.cvtColor(frame2, cv.COLOR_BGR2GRAY)
        gray2 = cv.GaussianBlur(gray2, (3, 3), 0)
        #finding mask between 2 consecutive frames
        deltaframe=cv.absdiff(gray1,gray2)
        # removing noise
        threshold = cv.threshold(deltaframe, 20, i, cv.THRESH_BINARY)[1]
        threshold = cv.dilate(threshold,None,iterations=5)
        #checking if all values are 0 or not
        zero_frame=len(gray2[gray2==0])
        if zero_frame<dimension:
            mask=np.maximum(mask,threshold)
    return mask

def masking():
    fontStyle = tkFont.Font(family="Lucida Grande", size=20)
    global masked_frames
    global ret
    
    output=[]
    skip=30
    #calculating first mask
    mask=calculate_first_mask(frames,skip)
    firstmask=np.zeros(frames[0].shape,dtype=np.uint8)
    #setting all non zero indexes of mask as 1 in firstmask
    firstmask[mask>0]=1
    #applying the mask on its frame
    actual_frame=frames[1]*firstmask
    dimension=frames[0].shape[0]*frames[0].shape[1]
    for i in range(len(frames)):
        temp=np.zeros((frames[0].shape),np.uint8)
        #setting all non zero indexes as 1
        temp[mask>0]=1
        #saving the mask applied on its frame in output
        output.append(frames[i]*temp)
        gray2 = cv.cvtColor(frames[i], cv.COLOR_BGR2GRAY)
        gray2 = cv.GaussianBlur(gray2, (3, 3), 0)
        zero_frame=len(np.where(gray2==0))
        #making a rectangle near the moving part
        countour,heirarchy = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        for j in countour:
            if cv.contourArea(j) < 50:
                continue
            (x, y, w, h) = cv.boundingRect(j)
            cv.rectangle(output[-1], (x, y), (x + w, y + h), (255, 0, 0), 2)
        #decreasing the mask as to remove the previous mask
        mask[mask>0]-=1
        #if its not the first frame
        if i>0:
            #calculate mask by subtracting 2 consecutive frame and removing noise
            deltaframe=cv.absdiff(gray1,gray2)
            threshold = cv.threshold(deltaframe, 20, skip, cv.THRESH_BINARY)[1]
            threshold = cv.dilate(threshold,None,iterations=20)
            zero_frame=len(gray2[gray2==0])
            if zero_frame<dimension:
                mask=np.maximum(mask,threshold)
        gray1=gray2
        #improving GUI part. showing percentage of frames masked
        if i%30==0:
            output_text='Frames Masked '+str(ceil(i*100/total_frames))+'%'
            label=Tk.Label(window, text=output_text,font=fontStyle).place(x=5,y=450)
        window.update()
    masked_frames=output
#    masked_frames=np.array(apply_mask(frames))

def playtogether():
    #this function plays 2 videos side by side
    global horizontal
    #concatinating frames horizontally
    horizontal=np.concatenate((frames,masked_frames),axis=2)
    #playing the video
    for i in horizontal:
        cv.imshow('img',i)
        if cv.waitKey(25) & 0xFF == ord('q'): 
            break
    

#Making the interface
length=600 #length of screen
width=500#width of screen
window=Tk.Tk()
window.title('Video segmentation')
window.geometry("600x500")
s = ttk.Style(window)
s.theme_use('clam')
#s.configure('flat.TButton', borderwidth=0)
s.configure('flat.TButton', relief='flat')
photo = PhotoImage(file = r"img.png") 
photo = photo.subsample(2,2)
photo1 = PhotoImage(file = r"fast1.png") 
photo1 = photo1.subsample(12,12)
#placing the images in top corners
lab1=Tk.Label(window, image=photo).place(x=0,y=0)
lab2=Tk.Label(window, image=photo1).place(x=490,y=0)
#placing buttons for functionality
btn2 = ttk.Button(text ='Load Video', width=18,command = lambda:detect_object()).place(x=length/2-length/8,y=200)
btn2 = ttk.Button(text ='Apply Masking',width=18, command = lambda:masking()).place(x=length/2-length/8,y=250)
btn3 = ttk.Button(text ='Play concatinated',width=18, command = lambda:playtogether()).place(x=length/2-length/8, y=300)
window.mainloop()
