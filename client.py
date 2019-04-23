#/usr/bin/python

import atexit
import socket
import cv2
import numpy as np
import cPickle as pickle
import struct
import sys

HOST ='192.168.0.24'
PORT = 1110
VIDFILE_NAME = "testFootage/test1_360p"
STRUCT_ARG = "I"
ROOM_NAME = str(sys.argv[1])


def exit_handler(s, cap):
    print("Closing connection and camera(s)")
    s.close()
    cv2.destroyAllWindows()
    cap.release()

#------------------MAIN EXECUTION------------------

# Set up socket and connect to server.
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((HOST,int(sys.argv[2])))
#s.sendall(struct.pack(STRUCT_ARG, len(str.encode(ROOM_NAME))),str.encode(ROOM_NAME));
s.sendall(str.encode(ROOM_NAME))

fgbg = cv2.createBackgroundSubtractorMOG2(100, 16, False)

# Send frame Data
cap = cv2.VideoCapture(0)#VIDFILE_NAME)
ret,frame = cap.read()

# Handle exit sequence
atexit.register(exit_handler, s, cap)


while ret:
    #ret,frame = cap.read()
    frame = cv2.resize(frame, (360, 240))
    fgmask = fgbg.apply(frame)
    count = np.count_nonzero(fgmask)

    data = pickle.dumps(frame, protocol = 2)

    if (count > 1000):
        #want to send the whole buffer at once
        try:
            s.settimeout(None)
            s.sendall(struct.pack(STRUCT_ARG, len(data))+data)
        except:
            print ("SENDING FAILED")
        
        s.settimeout(0.003)
        try:
            msg = str(s.recv(4096), 'utf-8')
            print(msg)
        except:
            pass
            

    ret,frame = cap.read()

