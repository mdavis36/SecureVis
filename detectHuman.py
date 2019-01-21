import cv2
from darkflow.net.build import TFNet
import numpy as np
import time

opt = {
    'model':'cfg/yolov1.cfg',
    'load':'bin/yolov1.weights',
    'threshold':0.01,
    'gpu':1.0
}

tfnet = TFNet(opt)

cap = cv2.VideoCapture('test480.mp4')
cols = [tuple(255 * np.random.rand(3)) for i in range(5)]


frame_count = 0
while (cap.isOpened()):
    stime = time.time()
    ret, frame = cap.read()
    frame_count += 1
    if ret:
        if frame_count%3 == 0:
            res = tfnet.return_predict(frame)
            for c, r in zip(cols, res):
                tl = (r['topleft']['x'], r['topleft']['y'])
                br = (r['bottomright']['x'], r['bottomright']['y'])
                label = r['label']
                if label == 'person':
                    frame = cv2.rectangle(frame, tl, br, c, 7)
                    frame = cv2.putText(frame, label, tl, cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,0), 2)
        cv2.imshow('frame', frame)
        print('FPS {:.1f}'.format(1/(time.time() - stime)))
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        cap.release()
        cv2.destroyAllWindows()
        break
