import cv2
import numpy as np
import IP

cap = cv2.VideoCapture('http://10.0.0.8:5000/?action=stream')

colour = input("Colour ('red' or 'blue'): ")

for i in range(5):
    _,temp = cap.read()


while True:

    _,img = cap.read()
    
    if colour == 'q':
        break

    masked_img = IP.masked(img,'red')
    opened_img = IP.opened(masked_img,21)
    cnt = IP.find_contour(opened_img)
    cnt_max,area = IP.maxContourArea(cnt,img)
    rx,ry = IP.centroid(cnt_max)
    
    (x,y),radius = cv2.minEnclosingCircle(cnt_max)
    center = (int(x),int(y))
    radius = int(radius)
    cv2.circle(img,center,radius,(0,255,0),2)
    cv2.rectangle(img, (rx - 2, ry - 2), (rx + 2, ry + 2), (0, 128, 255), -1)
        
    masked_img = IP.masked(img,'blue')
    opened_img = IP.opened(masked_img,21)
    cnt = IP.find_contour(opened_img)
    cnt_max,area = IP.maxContourArea(cnt,img)
    bx,by = IP.centroid(cnt_max)
    #print("Blue jewel's x-coordinate:",bx)
    (x,y),radius = cv2.minEnclosingCircle(cnt_max)
    center = (int(x),int(y))
    radius = int(radius)
    cv2.circle(img,center,radius,(0,255,0),2)
    cv2.rectangle(img, (bx - 2, by - 2), (bx + 2, by + 2), (0, 128, 255), -1)
    

    if colour=='red':
            if (int(rx)-int(bx))>0:
                    loc = 'right'
            else:
                    loc = 'left'

    else:
            if (int(bx)-int(rx))>0:
                    loc = 'right'
            else:
                    loc = 'left'

    print('Location of the JOI ({}):'.format(colour),loc)

    cv2.imshow('Detected Image',img)
    k = cv2.waitKey(1)

    if k == 'q':
        break
   
cv2.destroyAllWindows()
cap.release()

