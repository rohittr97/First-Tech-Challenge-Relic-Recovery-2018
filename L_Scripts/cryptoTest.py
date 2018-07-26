import IP as ip
import numpy as np
import cv2
'''
img = cv2.imread("Images/center 1.PNG")

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
cv2.imshow('center',hsv)

img = cv2.imread("Images/left 1.PNG")

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
cv2.imshow('left',hsv)

img = cv2.imread("Images/right 1.PNG")

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
cv2.imshow('right',hsv)
'''

img = cv2.imread("Testing/crypto center.png")
#print(np.shape(img))
x,y = 50,45
while x<img.shape[1]:
    cv2.line(img,(x,0),(x,img.shape[0]),(255,0,0),1,1)
    x+=49
while y<img.shape[0]:
    cv2.line(img,(0,y),(img.shape[1],y),(255,0,0),1,1)
    y+=50

'''
img = cv2.imread("Testing/crypto center.png")
print(np.shape(img))

img = cv2.imread("Testing/crypto right.png")
print(np.shape(img))

'''
mask = ip.masked(img,'blue')


open_img = ip.opened(mask,2)

cv2.imshow('mask',mask)
cv2.imshow('opened',open_img)
#open_img = open_img[70:120,45:145]
cnt = ip.find_contour(mask)
print(len(cnt))
cv2.imshow('grid',img)
cv2.waitKey(0)
cv2.destroyAllWindows()

