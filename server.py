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
from enum import Enum
from darkflow.net.build import TFNet


#==============================================================================

HOST = socket.gethostbyname('0.0.0.0')#'192.168.0.24'
PORT = int(sys.argv[1])
BUFFER_SIZE = 4096
MSG_DEF_SZ = 0
STRUCT_ARG = "I"
PERFORM_RECOGNITION = True


#==============================================================================

class ObjRecognition:
    def __init__(self):
        self.opt = {        
            'model':'cfg/yolov1.cfg',
            'load':'bin/yolov1.weights',
            'threshold':0.045,
            'gpu':1.0
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

#==============================================================================




#==============================================================================

class MsgType(Enum):
    NULL_MSG = -1
    PURE_MSG = 0
    MOTION_FRAME = 1
    TRIGGER_FRAME = 2




class Message:
    def __init__(self, raw_data, msg_size = MSG_DEF_SZ, msg_type = MsgType.PURE_MSG):
        self.size = msg_size
        self.type = msg_type
        self.msg_data = b""
        self.frame_data = b""
        self.room = -1
        self.cam  = -1

        self.data = raw_data
        if self.type != MsgType.PURE_MSG:
            self.frame_data = pickle.loads(raw_data[MSG_DEF_SZ:], encoding='latin1')
            self.msg_data = raw_data[:MSG_DEF_SZ]
        else:
            self.msg_data = raw_data 
        



class MsgHandler:

    def __init__(self):
        self.data = b""
        self.packet_size = struct.calcsize(STRUCT_ARG) 

    def getNextMsg(self, conn):
        # get the size of the data being sent over
        conn.settimeout(1.0)

        while len(self.data) < self.packet_size:
            try : 
                new_data = conn.recv(BUFFER_SIZE)
            except:
                return None
            self.data += new_data


        packed_msg_size = self.data[:self.packet_size]
        self.data = self.data[self.packet_size:]
        msg_size = struct.unpack(STRUCT_ARG,packed_msg_size)[0]

    
        # get the data from the struct that refers to the video.
        while len(self.data) < msg_size:
           self.data += conn.recv(BUFFER_SIZE)
        
        raw_frame = self.data[:msg_size]
        self.data = self.data[msg_size:]
   
        if (msg_size > 32): msg_type = MsgType.MOTION_FRAME
        else: msg_type = MsgType.PURE_MSG

        return Message(raw_frame, msg_size, msg_type)


#==============================================================================


def exit_handler(s):
    print("Closing Socket and windows")
    s.close()
    cv2.destroyAllWindows()




def new_client(conn,addr, objR):
    ROOM_NAME = str(conn.recv(BUFFER_SIZE), 'utf-8');
    msgHandler = MsgHandler()

    streamin_frame_data = False
    conn.setblocking(0) 

    if ("GUI" in ROOM_NAME):
        conn.send((threading.active_count()-2) +"\n")
    else:
        print (ROOM_NAME)

        now = datetime.datetime.now()
        #dateAndTime = now.strftime("%Y%m%d_%H%M")
        # Packet size will be no larger than the size of largest unsigned LONG value
        #fourcc = cv2.VideoWriter_fourcc(*'avc1')
        #outputVid = cv2.VideoWriter(str(ROOM_NAME, "utf-8") + "_"  +dateAndTime + "_output.avi",fourcc,20.0,(640,480))

        frame_count = 0
        last_frame_time = time.time()
        frame = np.zeros( (960, 1280, 3), dtype=np.uint8)
        while True:
            next_msg = msgHandler.getNextMsg(conn)

            if next_msg:
                if (next_msg.type != MsgType.PURE_MSG):
                    frame_count += 1 
                    if not streamin_frame_data:
                        streamin_frame_data = True 
                        print("Streaming Frame Data")

                    last_frame_time = time.time()

                    # Handle Frame Data Mesage
                    frame = next_msg.frame_data
                    frame = cv2.resize(frame,(1280,960))

                    if (PERFORM_RECOGNITION and frame_count % 10 == 1):
                        frame, res = objR.recog(frame)
                        if res:
                            print("TRIGGERED")
                            conn.send(str.encode("TRIGGEREDD!!!!"))




            if (time.time() - last_frame_time >= 3):
                frame = np.zeros((960, 1280, 3), dtype=np.uint8)
                if streamin_frame_data:
                    streamin_frame_data = False
                    print("Stopped Streaming Frame Data")
                    print(time.time() - last_frame_time )

            cv2.imshow(ROOM_NAME,frame)
            #outputVid.write(frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                conn.close()
                cv2.destroyWindow(ROOM_NAME)
                break
        

#-------------------MAIN EXECUTION-------------------
def main():
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST,int(sys.argv[1])))
    s.listen(10)
    
    objR = ObjRecognition()
    atexit.register(exit_handler, s)

    print ('Socket is now listening')

    while True:
        conn, addr = s.accept()
        _thread.start_new_thread(new_client,(conn,addr, objR));


if __name__ == "__main__" : main()
