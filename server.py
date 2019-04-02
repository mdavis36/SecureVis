#/usr/bin/python

import socket
import cv2
import pickle
import numpy as np
import struct
import sys
import _thread
import datetime
import os

HOST ='192.168.0.24'
PORT = int(sys.argv[1])
BUFFER_SIZE = 8192
STRUCT_ARG = "L"


def new_client(conn,addr):
    ROOM_NAME = conn.recv(BUFFER_SIZE);
    
    now = datetime.datetime.now()
    dateAndTime = now.strftime("%Y%m%d_%H%M")
    data = b""
    
    # Packet size will be no larger than the size of largest unsigned LONG value
    packet_size = struct.calcsize(STRUCT_ARG);
    fourcc = cv2.VideoWriter_fourcc(*'avc1')
    outputVid = cv2.VideoWriter(str(ROOM_NAME, "utf-8") + "_"  +dateAndTime + "_output.avi",fourcc,20.0,(640,480))


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

        if msg_size > 32:
            # Handle Frame Data Mesage
            frame = pickle.loads(raw_frame)
            frame = cv2.resize(frame,(640,480))
            cv2.imshow('frame',frame)
            outputVid.write(frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                conn.close()
                cv2.destroyWindow('frame')
                break
        #else:
            # Other Type Message
            


#-------------------MAIN EXECUTION-------------------

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST,int(sys.argv[1])))
s.listen(10)
print ('Socket is now listening')

while True:
    conn, addr = s.accept()
    _thread.start_new_thread(new_client,(conn,addr));

#cv2.destroyAllWindows()
s.close()


