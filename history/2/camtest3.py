import cv2
import numpy as np
 
# Read First Image
img1 = cv2.imread('C:/Python Project/capstone/0/car2.png')
 
# Read Second Image
img2 = cv2.imread('C:/Python Project/capstone/0/car2.png')
 
 
# concatenate image Horizontally
Hori = np.concatenate((img1, img2), axis=1)
 
# concatenate image Vertically
Verti = np.concatenate((img1, img2), axis=0)
 
cv2.imshow('HORIZONTAL', Hori)
cv2.imshow('VERTICAL', Verti)
 
cv2.waitKey(0)
cv2.destroyAllWindows()