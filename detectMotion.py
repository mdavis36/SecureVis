import cv2
import numpy as np

#cap = cv2.VideoCapture("testFootage/test1_360p")
cap = cv2.VideoCapture(0)

fgbg = cv2.createBackgroundSubtractorMOG2(100, 16, False)

frameCount = 0

while(1):

    ret, frame = cap.read()

    if not ret:
        break

    frameCount += 1
    resizedFrame = cv2.resize(frame, (0, 0), fx=0.50, fy=0.50)

    fgmask = fgbg.apply(frame)

    count = np.count_nonzero(fgmask)

    print('Frame: %d, Pixel Count: %d' % (frameCount, count))
    if (count > 5000):
        cv2.putText(frame, 'Motion Detected!', (10,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2, cv2.LINE_AA)

    cv2.imshow('Feed', frame)
    cv2.imshow('Mask', fgmask)

    k = cv2.waitKey(1) & 0xff
    if k ==27:
        break

cap.release()
cv2.destroyAllWindows()
