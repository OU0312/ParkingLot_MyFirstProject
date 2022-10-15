import cv2
import numpy as np
import matplotlib.pyplot as plt
import pytesseract
import serial
import time
import threading
from frametest import framein
    
def maincontrol() :
    py_serial = serial.Serial(
        
        # Window port
        port='COM4',
        
        # 보드 레이트 (통신 속도)
        baudrate=9600,
        
        timeout=10
    )
    
    db = []
    plt.style.use('dark_background')
    cam1 = cv2.VideoCapture(1)
    cam2 = cv2.VideoCapture(0)

    if cam1 == None or cam2 == None :
        print("No cam idiot")
    else :
        img_counter1 = 0
        img_counter2 = 0


        while True:
            isNextFrameAvail1, frame1 = cam1.read()
            isNextFrameAvail2, frame2 = cam2.read()
            if not isNextFrameAvail1 or not isNextFrameAvail2:
                break
            frame2Resized = cv2.resize(frame2,(frame1.shape[0],frame1.shape[1]))

            # ---- Option 1 ----
            #numpy_vertical = np.vstack((frame1, frame2))
            numpy_horizontal = np.hstack((frame1, frame2))

            cv2.imshow("Result", numpy_horizontal)
            
            ret, frame1 = cam1.read()
            ret2, frame2 = cam2.read()
            
            if not ret or not ret2:
                print("failed to grab frame")
                break
            #cv2.imshow("test", frame)

            k = cv2.waitKey(1)
            if k%256 == 27:
                # ESC pressed
                print("프로그램 종료중")
                break
            elif k%256 == ord('i'):
                camstate="IN"
                framein(camstate,frame1,img_counter1,py_serial,db)
                print(db)
            elif k%256 == ord('o'):
                camstate="OUT"
                framein(camstate,frame2,img_counter2,py_serial,db),
                print(db)