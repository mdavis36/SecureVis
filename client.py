#/usr/bin/python

import socket
import cv2
import numpy as np
import pickle
import struct
import sys

HOST ='127.0.0.1'
PORT = 1110
VIDFILE_NAME = "test480.mp4"
cap = cv2.VideoCapture(VIDFILE_NAME)
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((HOST,PORT))

ret,frame = cap.read()
while ret:
    #ret,frame = cap.read()
    data = pickle.dumps(frame)
    
    try:
        #want to send the whole buffer at once
        s.sendall(struct.pack("L", len(data))+data)
        print 'I AM HERE'
    except:
        print "SENDING FAILED"
    ret,frame = cap.read()
