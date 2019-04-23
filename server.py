#/usr/bin/python
import threading
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

threadCount = 0
room_list = []

room_cmd_queue = {}
room_cmd_queue_lock = threading.Lock()

#==============================================================================

class ObjRecognition:
    def __init__(self):
        self.opt = {        
            'model':'cfg/yolov1.cfg',
            'load':'bin/yolov1.weights',
            'threshold':0.045,
            'gpu':0.7
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
            self.msg_data = pickle.loads(raw_data[MSG_DEF_SZ:], encoding='latin1')
        


        



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
    global threadCount
    global room_list
    global room_cmd_queue

    ROOM_NAME = str(conn.recv(BUFFER_SIZE), 'utf-8');
    msgHandler = MsgHandler()
    
    stream_video = False
    streamin_frame_data = False
    triggered_active = False
    triggerable_found = False
    conn.setblocking(0) 

    if ("GUI" in ROOM_NAME):
        if "GET ROOM_NAMES" in ROOM_NAME:
            print(",".join(room_list))
            conn.send(str.encode(",".join(room_list) + "\n"))
        elif "GET ROOM_COUNT" in ROOM_NAME:
            print(threadCount)
            conn.send(str.encode(str(threadCount) + "\n"))
        elif "GET STREAM" in ROOM_NAME:
            with room_cmd_queue_lock:
                test_name = ROOM_NAME.split("GET STREAM ")[1][:-1]
                print(test_name)
                if test_name in room_cmd_queue:
                    room_cmd_queue[test_name].append(ROOM_NAME) 
                else:
                    room_cmd_queue[test_name] = [ROOM_NAME] 
                    
                print(room_cmd_queue)
            conn.send(str.encode("Opening Stream.\n"))
        else:
            print ("REQUEST ERROR : ", ROOM_NAME)
        #conn.send(str.encode(str(threading.active_count()-2) +"\n"))
    else:
        print (ROOM_NAME)
        room_list.append(ROOM_NAME)

        threadCount += 1
        #with room_cmd_queue_lock:
        #    room_cmd_queue[ROOM_NAME]=[]


        frame_count = 0
        last_frame_time = time.time()
        last_trigger_time = time.time()
        frame = np.zeros( (960, 1280, 3), dtype=np.uint8)
        output_file_name = ""
        while True:


            next_msg = msgHandler.getNextMsg(conn)

            if next_msg:
                if (next_msg.type != MsgType.PURE_MSG):
                    frame_count += 1 
                    if not streamin_frame_data:
                        streamin_frame_data = True 
                        print("Streaming Frame Data")
                        now = datetime.datetime.now()
                        dateAndTime = now.strftime("%Y%m%d_%H%M%S")
                        fourcc = cv2.VideoWriter_fourcc(*'avc1')
                        
                        output_file_name = ROOM_NAME + "_" + dateAndTime + "_output.avi"
                        outputVid = cv2.VideoWriter(output_file_name,fourcc,20,(1280,960))

                        triggerable_found = False

                    last_frame_time = time.time()

                    # Handle Frame Data Mesage
                    frame = next_msg.frame_data
                    frame = cv2.resize(frame,(1280,960))

                    if (PERFORM_RECOGNITION and frame_count % 1 == 0):
                        frame, res = objR.recog(frame)
                        if res:
                            last_trigger_time = time.time()
                            if not triggered_active:
                                triggered_active = True
                                triggerable_found = True
                                conn.send(str.encode("SET_MODE TRIGGERED TRUE"))
                        elif triggered_active and time.time() - last_trigger_time > 10:
                            triggered_active = False
                            conn.send(str.encode("SET_MODE TRIGGERED FALSE"))

                    if streamin_frame_data:  
                        outputVid.write(frame)
                        outputVid.write(frame)
                else:
                    print("PURE MSG")
                    strmsg = next_msg.msg_data
                    print(strmsg)
                    if "CLOSING" in strmsg:
                        print ("Closing Connetion to", strmsg.split(" ")[1:])
                        if stream_video:
                            cv2.destroyWindow(ROOM_NAME)
                        
                        threadCount -= 1
                        room_list.remove(ROOM_NAME)

            if(time.time() - last_frame_time >= 10):
                frame = np.zeros((960, 1280, 3), dtype=np.uint8)
                if streamin_frame_data:
                    streamin_frame_data = False
                    print("Stopped Streaming Frame Data")
                    print(time.time() - last_frame_time )
                    outputVid.release()
                    outputVid = None
                    if not triggerable_found:
                        os.system("rm " + output_file_name)

            cmd = ""
            with room_cmd_queue_lock:

                if ROOM_NAME in room_cmd_queue:
                    cmd_list = room_cmd_queue[ROOM_NAME]
                    if len(room_cmd_queue[ROOM_NAME]) > 0:
                        cmd = room_cmd_queue[ROOM_NAME].pop()
            
            if cmd != "":
                if "STREAM" in cmd:
                    stream_video = True


            if stream_video:
                cv2.namedWindow(ROOM_NAME, cv2.WINDOW_NORMAL)
                cv2.imshow(ROOM_NAME,frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                #conn.close()
                cv2.destroyWindow(ROOM_NAME)
                stream_video = False
                #print ("Closing Connetion to ", ROOM_NAME)
                #threadCount -= 1
                #break
        

#-------------------MAIN EXECUTION-------------------
def main():
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST,int(sys.argv[1])))
    s.listen(5)
   
    objR = None
    if PERFORM_RECOGNITION: objR = ObjRecognition()
    atexit.register(exit_handler, s)

    print ('Socket is now listening')

    while True:
        conn, addr = s.accept()
        _thread.start_new_thread(new_client,(conn,addr, objR));


if __name__ == "__main__" : main()
