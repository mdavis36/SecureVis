import cv2
from darkflow.net.build import TFNet

opt = {
    'model':'cfg/yolov1.cfg',
    'load':'bin/yolov1.weights',
    'threshold':0.3,
    'gpu':1.0
}

tfnet = TFNet(opt)
