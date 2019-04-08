#/usr/bin/python

import socket
import cv2
import numpy as np
import cPickle as pickle
import struct
import sys


HOST ='192.168.0.24'
PORT = 1110
VIDFILE_NAME = "testFootage/test480.mp4"
STRUCT_ARG = "I"

#ROOM_NAME = bytes(sys.argv[1], 'utf-8')
ROOM_NAME = str(sys.argv[1])

# Set up socket and connect to server.
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((HOST,int(sys.argv[2])))
s.sendall(str.encode(ROOM_NAME));


# Send frame Data
cap = cv2.VideoCapture(VIDFILE_NAME)
ret,frame = cap.read()
while ret:
    #ret,frame = cap.read()
    frame = cv2.resize(frame, (320, 240))
    data = pickle.dumps(frame, protocol = 2)
    print("Data len : ", len(str(data)))
#try:
    #want to send the whole buffer at once
    try:
        s.sendall(struct.pack(STRUCT_ARG, len(data))+data)
        print("Sending Frame")
        cv2.imshow('sending', frame) 
    except:
        print ("SENDING FAILED")
#iexcept:
    #print ("SENDING FAILED")
    ret,frame = cap.read()

cv2.destroyAllWindows()
