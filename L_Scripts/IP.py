import cv2
import numpy as np
#import matplotlib.pyplot as plt


def masked(img,colour):
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        #cv2.imshow("HSV",hsv)

        if colour == 'red':
                
                lower_red = np.array([0,50,50])
                upper_red = np.array([10,255,255])
                mask0 = cv2.inRange(hsv,lower_red,upper_red)

                lower_red = np.array([170,50,50])
                upper_red = np.array([180,255,255])
                mask1 = cv2.inRange(hsv,lower_red,upper_red)

                mask = mask0 + mask1

        elif colour == 'blue':

                lower_blue = np.array([100,50,50])
                upper_blue = np.array([130,255,255])

                mask = cv2.inRange(hsv,lower_blue,upper_blue)

        elif colour == 'yellow':

                #lower_yellow = np.array([5,50,235])
                #lower_yellow = np.array([15, 215, 240]) - actual
                #upper_yellow = np.array([20,240,250])
                #upper_yellow = np.array([20, 255, 255]) - actual
                lower_yellow = np.array([15, 140, 135]) 
                upper_yellow = np.array([25, 225, 210]) 

                mask = cv2.inRange(hsv,lower_yellow,upper_yellow)
                

        res = cv2.bitwise_and(img,img,mask = mask)

        return res


def opened(img,x,gray = True):

        kernel = np.ones((x,x),np.uint8)

        if gray:
                imgray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

        else:
                imgray = img

        imgo = cv2.morphologyEx(imgray, cv2.MORPH_OPEN, kernel)#opening

        return imgo

def closed(img,x,gray = True):

        kernel = np.ones((x,x),np.uint8)

        if gray:
                imgray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

        else:
                imgray = img

        imgo = cv2.morphologyEx(imgray, cv2.MORPH_CLOSE, kernel)#closing

        return imgo


def find_contour(img,tres = True):

        if tres:
                thresh = img

        else:
                imgray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
                _,thresh = cv2.threshold(imgray,127,255,0)
                
        _,contour,_=cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

        return contour


def maxContourArea(contours,img):

        #print("Entered maxContourArea")
        epsilon = 0.1*cv2.arcLength(contours[0],True)
        approx = cv2.approxPolyDP(contours[0],epsilon,True)
        area = cv2.contourArea(approx)
        i = contours[0]
        for cnt in contours:
                epsilon = 0.1*cv2.arcLength(cnt,True)
                approx_l = cv2.approxPolyDP(cnt,epsilon,True)
                ar = cv2.contourArea(approx_l)
                #print(ar)
                if ar>area:
                        area = ar
                        i = cnt
                        approx = approx_l
                        #print("Inside MaxArea approx if")

 
        return approx,area


def centroid(contour):

        M = cv2.moments(contour)
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])

        return cx,cy


def main1():
        
        img = cv2.imread('Images/jewelalign.png')
        colour = input("Colour ('red' or 'blue'): ")
        masked_img = masked(img,colour)
        opened_img = opened(masked_img,21)
        cnt = find_contour(opened_img)
        print("Number of contours:",len(cnt))
        if not len(cnt):
                print("No contour found!")
                exit(0)
        cnt_max,area = maxContourArea(cnt,img)
        cx,cy = centroid(cnt_max)
        contour_img = cv2.drawContours(img,cnt_max,0,(0,0,255),2)
        cv2.rectangle(contour_img, (cx - 2, cy - 2), (cx + 2, cy + 2), (0, 128, 255), -1)
        (x,y),radius = cv2.minEnclosingCircle(cnt_max)
        center = (int(x),int(y))
        radius = int(radius)
        circle_img = cv2.circle(img,center,radius,(0,255,0),2)

        #cv2.imshow('img',img)
        #plt.subplot(211),plt.imshow(img,'img')
        cv2.imshow('masked_img',masked_img)
        #plt.subplot(212),plt.imshow(masked_img,'masked_img')
        cv2.imshow('opened_img',opened_img)
        #plt.subplot(645),plt.imshow(opened_img,'opened_img')
        #cv2.imshow('contour_img',contour_img)
        #plt.subplot(647),plt.imshow(contour_img,'contour_img')
        cv2.imshow('Detected Image',circle_img)
        #plt.subplot(649),plt.imshow(circle_img,'circle_img')
        #plt.show()

        #print("Area:",area)

        cv2.waitKey(0)
        cv2.destroyAllWindows()

def main2(frame = 0,Try=True,colour='red'):

        if Try:
                img = cv2.imread('Images/center 1.PNG')
                colour = input("Colour ('red' or 'blue'): ")
        else:
                img = frame
        
        masked_img = masked(img,'red')
        opened_img = opened(masked_img,21)
        cnt = find_contour(opened_img)
        cnt_max,area = maxContourArea(cnt,img)
        rx,ry = centroid(cnt_max)
        print("Red jewel's x-coordinate:",rx)
        
        masked_img = masked(img,'blue')
        opened_img = opened(masked_img,21)
        cnt = find_contour(opened_img)
        cnt_max,area = maxContourArea(cnt,img)
        bx,by = centroid(cnt_max)
        print("Blue jewel's x-coordinate:",bx)

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

        print('Location of the JOI:',loc)

        if Try:
                cv2.imshow('Original Image',img)
                cv2.waitKey(0)
                cv2.destroyAllWindows()

        else:
                return loc

if __name__=='__main__':
        main2()
