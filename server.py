#/usr/bin/python

import atexit
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
from darkflow.net.build import TFNet

opt = {        
    'model':'cfg/yolov1.cfg',
    'load':'bin/yolov1.weights',
    'threshold':0.05,
    'gpu':1.0
}

tfnet = TFNet(opt)
cols = [tuple(255 * np.random.rand(3)) for i in range(5)]

HOST = socket.gethostbyname('0.0.0.0')#'192.168.0.24'
PORT = int(sys.argv[1])
BUFFER_SIZE = 4096
STRUCT_ARG = "I"

def exit_handler(s):
    print("Closing Socket and windows")
    s.close()
    cv2.destroyAllWindows()


def new_client(conn,addr):
    
    ROOM_NAME = conn.recv(BUFFER_SIZE);
    
    if ("GUI" in ROOM_NAME):
        conn.send((threading.active_count()-2) +"\n")
    else:
        print (str(ROOM_NAME, 'utf-8'))

        now = datetime.datetime.now()
        dateAndTime = now.strftime("%Y%m%d_%H%M")
        data = b""
        
        # Packet size will be no larger than the size of largest unsigned LONG value
        packet_size = struct.calcsize(STRUCT_ARG);
        fourcc = cv2.VideoWriter_fourcc(*'avc1')
        #outputVid = cv2.VideoWriter(str(ROOM_NAME, "utf-8") + "_"  +dateAndTime + "_output.avi",fourcc,20.0,(640,480))

        frame_count = 0


        while True:

            # get the size of the data being sent over
            while len(data) < packet_size:
                new_data = conn.recv(BUFFER_SIZE)
                data += new_data


            packed_msg_size = data[:packet_size]
            data = data[packet_size:]
            msg_size = struct.unpack(STRUCT_ARG,packed_msg_size)[0]


            # get the data from the struct that refers to the video.
            while len(data) < msg_size:
                data += conn.recv(BUFFER_SIZE)
            
            raw_frame = data[:msg_size]
            data = data[msg_size:]

            if (msg_size > 32):
                frame_count += 1
                print("Frame Data : ", frame_count)

                # Handle Frame Data Mesage
                frame = pickle.loads(raw_frame, encoding='latin1')
                frame = cv2.resize(frame,(640,480))
                res = tfnet.return_predict(frame)
                for c, r in zip(cols, res):
                    tl = (r['topleft']['x'], r['topleft']['y'])
                    br = (r['bottomright']['x'], r['bottomright']['y'])
                    label = r['label']
                    if label == 'person':
                        frame = cv2.rectangle(frame, tl, br, c, 7)
                        frame = cv2.putText(frame, label, tl, cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,0), 2)


            cv2.imshow(str(ROOM_NAME, 'utf-8'),frame)
            #outputVid.write(frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                conn.close()
                cv2.destroyWindow(str(ROOM_NAME, 'utf-8'))
                break
    

#-------------------MAIN EXECUTION-------------------

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST,int(sys.argv[1])))
s.listen(10)
print ('Socket is now listening')

atexit.register(exit_handler, s)

while True:
    conn, addr = s.accept()
    _thread.start_new_thread(new_client,(conn,addr));
