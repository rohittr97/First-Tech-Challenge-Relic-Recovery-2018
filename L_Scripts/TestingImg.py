import cv2
import IP as ip
import numpy as np

img = cv2.imread("Images/center picto real 5.jpg")
 
# convert the image to grayscale, blur it, and find edges
# in the image
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = cv2.bilateralFilter(gray, 11, 17, 17)
edged = cv2.Canny(gray, 30, 200)
cv2.imshow("Edge",edged)
cv2.waitKey(0)
cv2.destroyAllWindows()
