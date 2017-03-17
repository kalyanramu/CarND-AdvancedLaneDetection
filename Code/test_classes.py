# from Undistorter import Undistorter
# undistorter = Undistorter()
# print("Distortion Initiation Success")

# from Thresholder import Thresholder
# thresholder = Thresholder()
# print("Thresholding Initiation Success")

# from PerspectiveTransformer import PerspectiveTransformer
# ptransformer = PerspectiveTransformer()
# print("Perspective Transformer Initiation Success")

# from LaneDetector import LaneDetector
# laneDetector = LaneDetector()
# print("Lane Detector Initiation Success") 

# from LanePlotter import LanePlotter
# lanePlotter = LanePlotter()
# print("Lane Plotter Initiation Success") 

import cv2
import numpy as np
t=cv2.imread('warped.jpg')
img = cv2.cvtColor(t,cv2.COLOR_BGR2GRAY)
thresh_img = np.zeros_like(img)
thresh_img[img > 127] = 1

from LaneDetector import LaneDetector
laneDetector = LaneDetector()
print("Lane Detector Initiation Success") 
left_fit,right_fit = laneDetector.detect(thresh_img)
cv2.imwrite('detect.jpg',detect_img)

