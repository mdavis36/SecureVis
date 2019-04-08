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
import time

HOST = socket.gethostbyname('0.0.0.0')#'192.168.0.24'
PORT = int(sys.argv[1])
BUFFER_SIZE = 4096
STRUCT_ARG = "I"


def new_client(conn,addr):
    ROOM_NAME = conn.recv(BUFFER_SIZE);
    print (str(ROOM_NAME, 'utf-8'))

    now = datetime.datetime.now()
    dateAndTime = now.strftime("%Y%m%d_%H%M")
    data = b""
    
    # Packet size will be no larger than the size of largest unsigned LONG value
    packet_size = struct.calcsize(STRUCT_ARG);
    fourcc = cv2.VideoWriter_fourcc(*'avc1')
    #outputVid = cv2.VideoWriter(str(ROOM_NAME, "utf-8") + "_"  +dateAndTime + "_output.avi",fourcc,20.0,(640,480))


    while True:
        print (f"Packet Size {packet_size}")


        # get the size of the data being sent over
        while len(data) < packet_size:
            print(f"Data Length {len(data)}")
            new_data = conn.recv(BUFFER_SIZE)
            print(f"recv : {len(new_data)}")
            data += new_data

        
        packed_msg_size = data[:packet_size]
        data = data[packet_size:]
        msg_size = struct.unpack(STRUCT_ARG,packed_msg_size)[0]

        print (f"msg_size{int(msg_size)}")
        
        print(f"Data Length {len(data)}")

        # get the data from the struct that refers to the video.
        while len(data) < msg_size:
            data += conn.recv(BUFFER_SIZE)
        
        raw_frame = data[:msg_size]
        data = data[msg_size:]

        #if len(raw_frame) > 32 :
        # Handle Frame Data Mesage
        frame = pickle.loads(raw_frame, encoding='latin1')
        frame = cv2.resize(frame,(640,480))
        cv2.imshow(str(ROOM_NAME, 'utf-8'),frame)
        print("Frame Recieved.")
        #outputVid.write(frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            conn.close()
            cv2.destroyWindow(str(ROOM_NAME, 'utf-8'))
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


