import cv2
import numpy as np

capCamera = cv2.VideoCapture(0)
capVideo = cv2.VideoCapture(1)

while True:
    isNextFrameAvail1, frame1 = capCamera.read()
    isNextFrameAvail2, frame2 = capVideo.read()
    if not isNextFrameAvail1 or not isNextFrameAvail2:
        break
    frame2Resized = cv2.resize(frame2,(frame1.shape[0],frame1.shape[1]))

    # ---- Option 1 ----
    #numpy_vertical = np.vstack((frame1, frame2))
    #numpy_horizontal = np.hstack((frame1, frame2))
    numpy_horizontal = cv2.hconcat((frame1, frame2))

    cv2.imshow("Result", numpy_horizontal)
    cv2.waitKey(1)