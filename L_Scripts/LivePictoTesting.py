import cv2
import IP as ip
import numpy as np


cap = cv2.VideoCapture('http://10.0.0.8:5000/?action=stream')

ret, img = cap.read()
#img = cv2.imread("Images/center picto real 5.jpg")

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

cv2.imshow("HSV",hsv)

cnts = ip.find_contour(img,False)

print(len(cnts))
rect = []
for i in cnts:
    peri = cv2.arcLength(i, True)
    approx = cv2.approxPolyDP(i, 0.05 * peri, True)
    if len(approx)==4:
        rect.append(approx)
#rect,area = ip.maxContourArea(rect,img)
#epsilon = 0.1*cv2.arcLength(rect[0],True)
#approx = cv2.approxPolyDP(rect[0],epsilon,True)
print(len(rect))
area = cv2.contourArea(rect[0])
approx = rect[0]
i = rect[0]
for cnt in rect:
    #epsilon = 0.1*cv2.arcLength(cnt,True)
    #approx_l = cv2.approxPolyDP(cnt,epsilon,True)
    ar = cv2.contourArea(cnt)
    #print(ar)
    if ar>area:
        print("Inside")
        area = ar
        i = cnt
        approx = cnt

#print(area)
print(approx)
contour_img = cv2.drawContours(img,approx,0,(0,0,255),2)
cv2.imshow("Rect",contour_img)
pts = approx.reshape(4, 2)
rect = np.zeros((4, 2), dtype = "float32")
 
# the top-left point has the smallest sum whereas the
# bottom-right has the largest sum
s = pts.sum(axis = 1)
rect[0] = pts[np.argmin(s)]
rect[2] = pts[np.argmax(s)]
 
# compute the difference between the points -- the top-right
# will have the minumum difference and the bottom-left will
# have the maximum difference
diff = np.diff(pts, axis = 1)
rect[1] = pts[np.argmin(diff)]
rect[3] = pts[np.argmax(diff)]
(tl, tr, br, bl) = rect
widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
 
# ...and now for the height of our new image
heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
 
# take the maximum of the width and height values to reach
# our final dimensions
maxWidth = max(int(widthA), int(widthB))
maxHeight = max(int(heightA), int(heightB))
 
# construct our destination points which will be used to
# map the screen to a top-down, "birds eye" view
dst = np.array([
	[0, 0],
	[maxWidth - 1, 0],
	[maxWidth - 1, maxHeight - 1],
	[0, maxHeight - 1]], dtype = "float32")
 
# calculate the perspective transform matrix and warp
# the perspective to grab the screen
M = cv2.getPerspectiveTransform(rect, dst)
warp = cv2.warpPerspective(img, M, (maxWidth, maxHeight))
cv2.imshow("Warp",warp)
img = warp
x_s = int(img.shape[1]/4)
y_s = int(img.shape[0]/4)
x_i = x_s
y_i = y_s
print(img.shape[1])
print(img.shape[0])
x=x_s+int((10/931)*img.shape[1])
y=y_s+int((20/643)*img.shape[0])

while x<img.shape[1]:
    cv2.line(img,(x,0),(x,img.shape[0]),(255,0,0),1,1)
    x+=x_i

while y<img.shape[0]:
    cv2.line(img,(0,y),(img.shape[1],y),(255,0,0),1,1)
    y+=y_i

img_c = img[y_s+int((20/643)*img.shape[0])+y_i:y_s+int((20/643)*img.shape[0])+(2*y_i),x_s+int((10/931)*img.shape[1]):x_s+int((10/931)*img.shape[1])+x_i]

img_cm = ip.masked(img_c,"yellow")

img_co = ip.closed(img_cm,5)
img_co = ip.opened(img_co,5,False)

cnt = ip.find_contour(img_co)

print(len(cnt))

if len(cnt)==3:
    print("left")
elif len(cnt)==6:
    print("right")
elif len(cnt)==5:
    print("center")

cv2.imshow("Grid",img)
cv2.imshow("Cropped",img_c)
cv2.imshow("Masked",img_cm)
cv2.imshow("Opened",img_co)
cv2.waitKey(0)
cv2.destroyAllWindows()
