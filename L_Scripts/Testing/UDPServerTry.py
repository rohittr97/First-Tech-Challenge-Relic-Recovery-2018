#UdpReplyServer.py

import socket
import cv2
import numpy as np

 

sock = socket.socket (socket.AF_INET, socket.SOCK_DGRAM)

sock.bind (("127.0.0.1", 1234))

#data = 'Nothing Recieved'
i=1

while i:

    data, addr = sock.recvfrom (1024)

    img = np.frombuffer(data, dtype=np.uint8)

    #print("Message: ", data.decode('utf-8'))

    cv2.imshow('Recieved Image',img)

    i=0

    

 

