#/usr/bin/python
import cv2
import numpy as np

from darkflow.net.build import TFNet


class ObjRecognition:
    def __init__(self):
        self.opt = {        
            'model':'cfg/yolov1.cfg',
            'load':'bin/yolov1.weights',
            'threshold':0.045,
            'gpu':0.7
        }
        self.tfnet = TFNet(self.opt)
        self.cols = [tuple(255 * np.random.rand(3)) for i in range(5)]


    def recog(self, frame, triggerables = ('person')):
        result = False
        res = self.tfnet.return_predict(frame)

        for c, r in zip(self.cols, res):
            tl = (r['topleft']['x'], r['topleft']['y'])
            br = (r['bottomright']['x'], r['bottomright']['y'])
            label = r['label']
        
            if label == triggerables:
                result = True
                frame = cv2.rectangle(frame, tl, br, c, 7)
                frame = cv2.putText(frame, label, tl, cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,0), 2)
        
        return frame, result



class ObjRecognitionV34:
    def __init__(self):
        pass

    def recog(self, frame, triggerables = ('person')):
        pass


