#Coloumn Detection

import IP as ip
import cv2
import socket
import json
import numpy as np

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
add = '192.168.1.101'
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
                if ar>40000:
                    a.append(cnt)
 
        #print(ac)
        return a,ac

try:

    if True:

        kernel = np.ones((21,21),np.uint8)

        _,frame = cap.read()

        mask = ip.masked(frame,'blue')

        
        #op = ip.closed(mask,21)

        op = mask[:int(mask.shape[0]/2)][:]
        op = ip.closed(op,51)
        #op = cv2.dilate(op,kernel,iterations = 1)

        cnt = ip.find_contour(op)
        if len(cnt)>0:
            cnt,ar = AbContourArea(cnt)

        #cent = []

        #for i in range(len(cnt)):
            #cent.append(ip.centroid(cnt[i]))
            #cv2.rectangle(op, (int(cent[i][0]) - 2, int(cent[i][1]) - 2), (int(cent[i][0]) + 2, int(cent[i][1]) + 2), (0, 128, 255), -1)

        #print(len(cnt))

        msg = {'done':True}
        msg_es = json.dumps(msg)
        msg_eb = str.encode(msg_es)
            
        while len(cnt)<2:
            print(len(cnt))
            sock.sendto(msg_eb, (add, 1234))
            cv2.imshow('Video',mask)
            cv2.imshow('Video 2',op)
            cv2.waitKey(1)
            _,frame = cap.read()

            mask = ip.masked(frame,'blue')

            #op = ip.closed(mask,21)

            op = mask[:int(mask.shape[0]/2)][:]
            op = ip.closed(op,51)

            cnt = ip.find_contour(op)
            #if len(cnt)>0:
                #cnt,ar = AbContourArea(cnt)

        print('1 = ',len(cnt))

        while len(cnt)>1 or len(cnt)==0:
            sock.sendto(msg_eb, (add, 1234))
            cv2.imshow('Video',mask)
            cv2.imshow('Video 2',op)
            cv2.waitKey(1)
            _,frame = cap.read()

            mask = ip.masked(frame,'blue')

            op = mask[:int(mask.shape[0]/2)][:]
            op = ip.closed(op,51)

            cnt = ip.find_contour(op)
            #if len(cnt)>0:
                #cnt,ar = AbContourArea(cnt)
                
        print('2 = ', len(cnt))

        while len(cnt)<2:
            print(len(cnt))
            sock.sendto(msg_eb, (add, 1234))
            cv2.imshow('Video',mask)
            cv2.imshow('Video 2',op)
            cv2.waitKey(1)
            _,frame = cap.read()

            mask = ip.masked(frame,'blue')

            op = mask[:int(mask.shape[0]/2)][:]
            op = ip.closed(op,51)

            cnt = ip.find_contour(op)
            #if len(cnt)>0:
                #cnt,ar = AbContourArea(cnt)

        print('3 = ',len(cnt))

        while len(cnt)>1 or len(cnt)==0:
            sock.sendto(msg_eb, (add, 1234))
            cv2.imshow('Video',mask)
            cv2.imshow('Video 2',op)
            cv2.waitKey(1)
            _,frame = cap.read()

            mask = ip.masked(frame,'blue')

            op = mask[:int(mask.shape[0]/2)][:]
            op = ip.closed(op,51)

            cnt = ip.find_contour(op)
            #if len(cnt)>0:
                #cnt,ar = AbContourArea(cnt)
                
        print('4 = ', len(cnt))

        
        msg = {'done':False}
        msg_es = json.dumps(msg)
        msg_eb = str.encode(msg_es)
        sock.sendto(msg_eb, (add, 1234))

        dnt = True

        while dnt:
            sock.settimeout(0.3)
            try:
                data = sock.recv(1024)
                dnt = False

            except socket.timeout:
                sock.sendto(msg_eb, (add, 1234))
                
        cv2.imshow('Video',mask)
        cv2.imshow('Video 2',op)

        cv2.waitKey(0)

finally:

    cv2.destroyAllWindows()
