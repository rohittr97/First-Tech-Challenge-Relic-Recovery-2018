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
(_,cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:10]
screenCnt = None
# loop over our contours
for c in cnts:
	# approximate the contour
	peri = cv2.arcLength(c, True)
	approx = cv2.approxPolyDP(c, 0.02 * peri, True)
 
	# if our approximated contour has four points, then
	# we can assume that we have found our screen
	if len(approx) == 4:
		screenCnt = approx
		break

print(len(screenCnt))

cv2.drawContours(img, [screenCnt], -1, (0, 255, 0), 3)
cv2.imshow("Image", img)
# now that we have our screen contour, we need to determine
# the top-left, top-right, bottom-right, and bottom-left
# points so that we can later warp the image -- we'll start
# by reshaping our contour to be our finals and initializing
# our output rectangle in top-left, top-right, bottom-right,
# and bottom-left order
pts = screenCnt.reshape(4, 2)
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
# now that we have our rectangle of points, let's compute
# the width of our new image
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
cv2.imshow("Cropped",warp)
img = warp
x_s = int(img.shape[1]/4)
y_s = int(img.shape[0]/4)
x_i = x_s
y_i = y_s
print(img.shape[1])
print(img.shape[0])
x=x_s+int((10/931)*img.shape[1])
y=y_s+int((50/643)*img.shape[0])

while x<img.shape[1]:
    cv2.line(img,(x,0),(x,img.shape[0]),(255,0,0),1,1)
    x+=x_i

while y<img.shape[0]:
    cv2.line(img,(0,y),(img.shape[1],y),(255,0,0),1,1)
    y+=y_i

img_c = img[y_s+int((50/643)*img.shape[0])+y_i:y_s+int((50/643)*img.shape[0])+(2*y_i),x_s+int((10/931)*img.shape[1]):x_s+int((10/931)*img.shape[1])+x_i]

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
