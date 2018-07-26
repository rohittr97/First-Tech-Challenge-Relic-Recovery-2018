import cv2
import IP as ip
import numpy

img = cv2.imread("Images/right picto.png")

x_s = int(img.shape[1]/4)
y_s = int(img.shape[0]/4)
x_i = x_s
y_i = y_s
print(img.shape[1])
print(img.shape[0])
x=x_s-int((12/931)*img.shape[1])
y=y_s+int((70/643)*img.shape[0])

while x<img.shape[1]:
    cv2.line(img,(x,0),(x,img.shape[0]),(255,0,0),1,1)
    x+=x_i

while y<img.shape[0]:
    cv2.line(img,(0,y),(img.shape[1],y),(255,0,0),1,1)
    y+=y_i

img_c = img[y_s+int((70/643)*img.shape[0])+y_i:y_s+int((70/643)*img.shape[0])+(2*y_i),x_s-int((12/931)*img.shape[1]):x_s-int((12/931)*img.shape[1])+x_i]

img_cm = ip.masked(img_c,"yellow")

img_co = ip.closed(img_cm,5)
#img_co = ip.opened(img_co,5,False)

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
