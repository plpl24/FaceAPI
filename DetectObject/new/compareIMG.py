import cv2
import numpy as np
img1 = cv2.imread("face2.jpg")
img2 = cv2.imread("face.jpg")

hist1 = cv2.calcHist([img1], [0], None, [256], [0, 256])
hist2 = cv2.calcHist([img2], [0], None, [256], [0, 256])


ret = cv2.compareHist(hist1, hist2, 0)
print(ret)