from flask import Flask, render_template
import os
import threading , time
import cv2
import numpy as np

webcam_flag = False
def webcamCap(stop):
    cap = cv2.VideoCapture(0)
    while(True):
        global webcam_flag
        ret , frame = cap.read()
        #   RGB -> Grey Conversion (Optional)
        gray_frame = cv2.cvtColor(frame , cv2.COLOR_BGR2GRAY)
        
        cv2.imshow('Grey SelfCam' , gray_frame)
        global webcam_flag
        print(webcam_flag)
        if stop():
            break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()