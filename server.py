#/usr/bin/python

import socket
import cv2
import pickle
import numpy as np
import struct
import sys
import thread
import datetime
import os

HOST ='127.0.0.1'
PORT = 1110
BUFFER_SIZE = 8192
STRUCT_ARG = "L"


def new_client(conn,addr):
    #path = os.getcwd()
    ROOM_NAME = conn.recv(BUFFER_SIZE);
    #print(ROOM_NAME)
    

    
    now = datetime.datetime.now()
    dateAndTime = now.strftime("%Y%m%d_%H%M")
    data = ""
    # Packet will be the size of largest unsigned LONG value
    packet_size = struct.calcsize(STRUCT_ARG);
    fourcc = cv2.VideoWriter_fourcc(*'avc1')
    outputVid = cv2.VideoWriter(ROOM_NAME+ "_"  +dateAndTime + "_output.avi",fourcc,20.0,(640,480))
    while True:
        # get the size of the data being sent over
        while len(data) < packet_size:
            data += conn.recv(BUFFER_SIZE)
        packed_msg_size = data[:packet_size]
        data = data[packet_size:]
        msg_size = struct.unpack(STRUCT_ARG,packed_msg_size)[0]
        # get the data from the struct that refers to the video.
        while len(data) < msg_size:
            data += conn.recv(BUFFER_SIZE)
        raw_frame = data[:msg_size]
        data = data[msg_size:]

        frame = pickle.loads(raw_frame)
        frame = cv2.resize(frame,(640,480))
        #cv2.imshow('frame',frame)
        outputVid.write(frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            conn.close()
            break


s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((HOST,PORT))
s.listen(10)
print 'Socket is now listening'




while True:
    conn, addr = s.accept()
    thread.start_new_thread(new_client,(conn,addr));

#cv2.destroyAllWindows()
s.close()


