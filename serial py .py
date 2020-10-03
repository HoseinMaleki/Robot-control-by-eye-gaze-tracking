import cv2
import argparse
import imutils
import numpy as np
import matplotlib.pyplot as plt 
import matplotlib.image as mpimg
import serial
import time



cap = cv2.VideoCapture(1)
thresh=70
sens=100
#........................................Welcome..................................................


def nothing(x):
    pass

def calibration():
    print("welcome \n Calibration Mode \n Place your pupil inside the blue circle")
    print(" after calibration press \'q\' to continue")
    while(True):
        ret,eye_clb=cap.read()
        eye_clb= cv2.flip(eye_clb, -1) #flip vertical
        eye_clb= cv2.flip(eye_clb, 1) # flip horizontal
        eye_clb=cv2.resize(eye_clb,(250,180),interpolation = cv2.INTER_AREA)  # resize cap
        eye_clb=cv2.circle(eye_clb, (175,55), 20, (0, 255, 0),2)  #draw circle for Calibrate
        eye_clb_2=eye_clb[20:90,125:220]
        cv2.imshow('eye_calibrate',eye_clb)
        cv2.imshow('eye_calibrate_resize',eye_clb_2)
        cv2.moveWindow('eye_calibrate',1120,200)
        cv2.moveWindow('eye_calibrate_resize',1400,200)
        
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

def pupil_detect_calibration():
    print("Pupil detect calibration Mode\n adjust threshold and sensivity \n after calibration press \'q\' to continue ")
    cv2.namedWindow("pupil detect calibration", cv2.WINDOW_NORMAL)
    cv2.createTrackbar('threshold','pupil detect calibration',0,255,nothing)
    cv2.createTrackbar('sensevity','pupil detect calibration',0,1000,nothing)

    global thresh
    global sens

    while(True):
        ret, eye = cap.read()  # read capture
        eye= cv2.flip(eye, -1) #flip vertical
        eye= cv2.flip(eye, 1)   # flip horizontal
        eye=cv2.resize(eye,(250,180),interpolation = cv2.INTER_AREA)  # resize cap
        eye=eye[20:90,125:220]
        # image processing ........................................ض.....................................
        gray_eye = cv2.cvtColor(eye,cv2.COLOR_BGR2GRAY)
        gray_eye = cv2.GaussianBlur(gray_eye, (9, 9), 0)
        gray_eye = cv2.medianBlur(gray_eye, 1)
        ret,threshold = cv2.threshold(gray_eye,int(thresh),255, cv2.THRESH_BINARY_INV)
        cv2.imshow('threshold',threshold)
        # cv2.imshow('eye',gray_eye)
        # cv2.imshow('eye1',eye)

        thresh = cv2.getTrackbarPos('threshold','pupil detect calibration')
        sens = cv2.getTrackbarPos('sensevity','pupil detect calibration')
        cv2.moveWindow('threshold',1550,200)
        cv2.moveWindow('pupil detect calibration',1220,200)
        # image processing .............................................................................

        cnts = cv2.findContours(threshold.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        #Find center of contours........................................................................
        for c in cnts :
            if(cv2.contourArea(c)<sens): 
                continue
            M = cv2.moments(c)
            cX = (int(M["m10"] / M["m00"])) if M["m00"] else 0
            cY = (int(M["m01"] / M["m00"])) if M["m00"] else 0
            cv2.drawContours(eye,c, -1, (0, 255, 0), 1)
            cv2.drawContours(eye,[c], -1, (0, 255, 0), 1)
            cv2.circle(eye, (cX, cY), 5, (255, 255, 255), -1)
            
        cv2.imshow("pupil detect calibration", eye)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

# def serial():
#     ser = serial.Serial('COM3', 9600, timeout=1)
#     while True:
#         A = input ("enter your command: \n")
#         if (A=='H' or A=='h'):
#             ser.write(b'H')
#         elif (A=='L' or A=='l'):
#             ser.write(b'L')
#     ser.close()

def pupil_detect_data():
    print("Pupil detect Mode\n press \'q\'  for exit  ")
    
    cv2.namedWindow("pupil detect", cv2.WINDOW_NORMAL)
    ser = serial.Serial('COM3', 9600, timeout=1)
    # ser.write(b'1')

    while(True):
        ret, eye = cap.read()  # read capture
        eye= cv2.flip(eye, -1) #flip vertical
        eye= cv2.flip(eye, 1)   # flip horizontal
        eye=cv2.resize(eye,(250,180),interpolation = cv2.INTER_AREA)  # resize cap
        eye=eye[20:90,125:220]
        # image processing ........................................ض.....................................
        gray_eye = cv2.cvtColor(eye,cv2.COLOR_BGR2GRAY)
        gray_eye = cv2.GaussianBlur(gray_eye, (9, 9), 0)
        gray_eye = cv2.medianBlur(gray_eye, 1)
        ret,threshold = cv2.threshold(gray_eye,int(thresh),255, cv2.THRESH_BINARY_INV)
        cv2.imshow('threshold',threshold)
        # cv2.imshow('eye',gray_eye)
        # cv2.imshow('eye1',eye)
        cv2.moveWindow('threshold',1550,200)
        cv2.moveWindow('pupil detect',1220,200)
        # image processing .............................................................................

        cnts = cv2.findContours(threshold.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        #Find center of contours........................................................................
        for c in cnts :
            if(cv2.contourArea(c)<sens): 
                continue
            M = cv2.moments(c)
            cX = (int(M["m10"] / M["m00"])) if M["m00"] else 0
            cY = (int(M["m01"] / M["m00"])) if M["m00"] else 0
            cv2.drawContours(eye,c, -1, (255, 255, 255), 1)
            cv2.drawContours(eye,[c], -1, (255, 255, 255), 1)
            cv2.circle(eye, (cX, cY), 5, (0, 255, 0), -1)
        
        # graph lines 
        cv2.line(eye,(48,0),(48,70),(255, 255, 255),1)
        cv2.line(eye,(36,0),(36,70),(255, 255, 255),1)  
        cv2.line(eye,(24,0),(24,70),(255, 255, 255),1)
        cv2.line(eye,(12,0),(12,70),(255, 255, 255),1)
        cv2.line(eye,(60,0),(60,70),(255, 255, 255),1)
        cv2.line(eye,(72,0),(72,70),(255, 255, 255),1)
        cv2.line(eye,(84,0),(84,70),(255, 255, 255),1)
        # cv2.line(eye,(0,35),(95,35),(255, 255, 255),1)
        #if---------------------------------------------------------
        
        # print("[{0},{1}]".format(cX,cY))
        # ser = serial.Serial('COM3', 9600, timeout=1)
        # ser.open()
        
        if (0<int(cX)<=12):
            ser.write(b'23')
            time.sleep(1)
        elif(12<int(cX)<=24):
            ser.write(b'45')
            time.sleep(1)
        elif(24<int(cX)<=36):
            ser.write(b'68')
            time.sleep(1)
        elif(36<int(cX)<=60):
            ser.write(b'90')
            time.sleep(1)
        elif(60<int(cX)<=72):
            ser.write(b'113')
            time.sleep(1)
        elif(72<int(cX)<=84):
            ser.write(b'135')
            time.sleep(1)
        elif(84<int(cX)<=95):
            ser.write(b'158')
            time.sleep(1)

        # rows,cols,_ = eye.shape
        # print("rows is {0} and cols is {1}" .format(rows,cols))      #Print image specifications
        #if----------------------------------------------------------
        cv2.imshow("pupil detect", eye)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            ser.close()
            break
#...................................................................................................



calibration()
pupil_detect_calibration()
pupil_detect_data()

cap.release()
cv2.destroyAllWindows()