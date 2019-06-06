import cv2
import numpy as np
import time
import datetime

# Choose if the resulting video should be displayed or stored to disk.
store_video = False
# Select video to analyse:
cap = cv2.VideoCapture('movies/Location1_take2.avi')
afile = open('test_d.txt', 'w')
afile.write('time\tu100\tu250\tu500\tu1000\tstor\n')
if store_video:
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('output_2.avi', fourcc, 10.0, (640, 480))


def check_size(frame, contours):
    """Checks the different areas sizes.

    Parameters
    ----------
    frame: numpy.ndarray
    contours: list

    Returns
    -------
    frame: numpy.ndarray
    """
    l100 = 0
    l250 = 0
    l500 = 0
    l1000 = 0
    l2000 = 0
    l_contours = []
    for poly in contours:
        area = cv2.contourArea(poly)
        if area > 50:
            l_contours.append(poly)
            if area < 100:
                l100 += 1
            elif area < 250:
                l250 += 1
            elif area < 500:
                l500 += 1
            elif area < 1000:
                l1000 += 1
            else:
                l2000 += 1
    cv2.drawContours(frame, l_contours, -1, (0, 255, 0), 3)
    line = '{}\t{}\t{}\t{}\t{}\t'.format(l100, l250, l500, l1000, l2000)
    afile.write(datetime.datetime.now().isoformat() + '\t' + line + '\n')
    return frame


def hsv_filtering(frame):
    """Check the frame and tries to identifies the potatoes. The result of the
    filtering is either displayed on the screen or stored to disk depending on
    the parameter store_video

    Parameters
    ----------
    frame: numpy.ndarray

    Returns
    -------

    """
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_blue = np.array([20, 00, 30])
    upper_blue = np.array([80, 100, 100])
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    __, contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    frame = check_size(frame, contours)
    if store_video:
        out.write(frame)
    else:
        cv2.imshow('mask', mask)
        cv2.imshow('result', frame)
        time.sleep(0.5)
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            return


font = cv2.FONT_HERSHEY_SIMPLEX
running = True
i = 0
while running:
    _, frame = cap.read()
    #To kill script when runs out of frames
    if frame is None:
        running = False
        continue
    #Filter the time when potatoes is passing.
    i += 1
    #print(i)
    if 80 < i < 200:
        hsv_filtering(frame)
        
cv2.destroyAllWindows()
cap.release()
