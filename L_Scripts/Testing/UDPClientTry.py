#UdpClient.py

import socket
#import cv2
#import numpy as np

#img = cv2.imread('with 3x3 kernel.png')

#img1 = img.tobytes()

#print(type(img1))


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#msg = img1


while True:

    msg = str.encode(input('Message? : '))
    sock.sendto(msg, ("127.0.0.1", 1234))
    
