#Jewel

import cv2
import IP as ip
import socket
import json
from time import sleep

change = True

add = '192.168.7.2'

color = input("Alliance: ")

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

cap = cv2.VideoCapture('http://{}:5000/?action=stream'.format(add))

ret, frame = cap.read()

print(ret)

cv2.imshow("Frame",frame)
def forward():

  return {'p1':100,'p2':0,'p3':100,'p4':0,'flipper':[0,0],'grabber':[0,0],'ch':change, 'jewelArm':1} 

def backward():

  return {'p1':0,'p2':100,'p3':0,'p4':100,'flipper':[0,0],'grabber':[0,0],'ch':change, 'jewelArm':1}

def none():

  return {'p1':100,'p2':0,'p3':100,'p4':0,'flipper':[0,0],'grabber':[0,0],'ch':change, 'jewelArm':0} 

def stop():

  return {'p1':0,'p2':0,'p3':0,'p4':0,'flipper':[0,0],'grabber':[0,0],'ch':change, 'jewelArm':0} 


#cv2.imshow('Video', frame)
try:

  loc = ip.main2(frame,False,color)

  if loc == "right":
    msg = backward()

  else:
    msg = forward()

except Exception as e:

  msg = none()
  print(e)

msg_es = json.dumps(msg)
msg_eb = str.encode(msg_es)
sock.sendto(msg_eb, (add, 1234))

sleep(2)

msg_es = json.dumps(stop())
msg_eb = str.encode(msg_es)
sock.sendto(msg_eb, (add, 1234))
cv2.waitKey(0)
cv2.destroyAllWindows()
