#!/opt/local/bin/python
# -*- coding: utf-8 -*-
import cv2
import numpy as np

CAM_ID = 0

#Open the CAM
cap = cv2.VideoCapture(CAM_ID) #카메라 생성

#Check that the camera is opened
if cap.isOpened() == False: #카메라 생성 확인
    print ('Can\'t open the CAM(%d)' % (CAM_ID))
    exit()

#create the window & change the window size
#윈도우 생성 및 사이즈 변경
titles = ['orig','th1','th2','th3']

for t in titles:
    cv2.namedWindow(t)

while(True):
    #read the camera image
    #카메라에서 이미지 얻기
    ret, frame = cap.read()

    # 이미지 높이
    height = frame.shape[0]
    # 이미지 넓비
    width = frame.shape[1]
    # 이미지 색
    depth = frame.shape[2]

    grayframe = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    grayframe = cv2.equalizeHist(grayframe)

    blur = cv2.medianBlur(grayframe,5)
    ret, th1 = cv2.threshold(blur, 127, 255, cv2.THRESH_BINARY)
    th2 = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
    th3 = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

    # 화면 표시
    cv2.imshow(titles[0],frame)
    cv2.imshow(titles[1],th1)
    cv2.imshow(titles[2],th2)
    cv2.imshow(titles[3],th3)

    #wait keyboard input until 10ms
    #10ms 동안 키입력 대기
    if cv2.waitKey(1) == 27:
        break;

#close the window
#윈도우 종료
cap.release()
cv2.destroyAllWindows()
