#/usr/bin/python

import socket
import cv2
import numpy as np
import pickle
import struct
import sys


HOST ='192.168.0.24'
PORT = 1110
VIDFILE_NAME = "testFootage/test480.mp4"
ROOM_NAME = bytes(sys.argv[1], 'utf-8')


# Set up socket and connect to server.
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((HOST,int(sys.argv[2])))
s.sendall(ROOM_NAME);


# Send frame Data
cap = cv2.VideoCapture(VIDFILE_NAME)
ret,frame = cap.read()
while ret:
    #ret,frame = cap.read()
    data = pickle.dumps(frame)
    
    try:
        #want to send the whole buffer at once
        s.sendall(struct.pack('L', len(data))+data)
        #print 'I AM HERE'
    except:
        print ("SENDING FAILED")
    ret,frame = cap.read()

cv2.destroyAllWindows()
