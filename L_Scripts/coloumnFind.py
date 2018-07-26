import IP as ip
import cv2

cap = cv2.VideoCapture('http://192.168.1.101:5000/?action=stream')

def AbContourArea(contours):

        #print("Entered maxContourArea")
        epsilon = 0.1*cv2.arcLength(contours[0],True)
        approx = cv2.approxPolyDP(contours[0],epsilon,True)
        area = cv2.contourArea(approx)
        i = contours[0]
        a = []
        ac = []
        for cnt in contours:
                epsilon = 0.1*cv2.arcLength(cnt,True)
                approx_l = cv2.approxPolyDP(cnt,epsilon,True)
                ar = cv2.contourArea(approx_l)
                ac.append(ar)
                #print(ar)
                if ar>10000:
                    a.append(cnt)
 
        #print(ac)
        return a,ac



try:

    while True:

        _,frame = cap.read()

        mask = ip.masked(frame,'blue')

        #op = ip.closed(mask,21)

        op = ip.closed(mask,51)
        op = op[:int(op.shape[0]/3)][:]

        #op = cv2.dilate(op,21,iterations = 1)
        
        

        cnt = ip.find_contour(op)

        #cent = []

        #or i in range(len(cnt)):
            #cent.append(ip.centroid(cnt[i]))
            #cv2.rectangle(op, (int(cent[i][0]) - 2, int(cent[i][1]) - 2), (int(cent[i][0]) + 2, int(cent[i][1]) + 2), (0, 128, 255), -1)

        print(len(cnt))
        #n_cnt,ar = AbContourArea(cnt)
        #print(len(n_cnt),ar)

        cv2.imshow('Video',op)

        cv2.waitKey(1)

finally:

    cv2.destroyAllWindows()
