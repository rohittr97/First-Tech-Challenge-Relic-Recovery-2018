import cv2
import IP as ip

cap = cv2.VideoCapture('http://192.168.7.2:5000/?action=stream')

done = True

while done:
  ret, frame = cap.read()
  if not ret:
      print(ret)
      continue
  #f = cv2.flip(frame,0)
  hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
  cv2.imshow('Video', frame)
  #cv2.imshow('Vid', frame)
  #ip.main2(frame,False)

  if cv2.waitKey(1) == 27:
    cv2.destroyAllWindows()
    done = False
    #exit(0)
