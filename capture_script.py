import cv2
import time
import datetime


cap = cv2.VideoCapture(0)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output_{t}.avi'.format(t=datetime.datetime.now().isoformat()),fourcc, 10.0, (640,480))
t0=time.time()    
font = cv2.FONT_HERSHEY_SIMPLEX
while True:
    _, frame = cap.read()
    t1 = datetime.datetime.now().isoformat()
    cv2.putText(frame, t1, (30, 470), font, 0.5, (255,0,0), 1,  cv2.LINE_AA)
    out.write(frame)
    if (time.time()-t0) > 25:
        break

cv2.destroyAllWindows()
cap.release()
