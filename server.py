#/usr/bin/python
import atexit
import cv2
import datetime
import numpy as np
import os
import socket
import struct
import sys
import _thread
import threading
import time

from Const import *
from Messaging import *
from ObjRecognition import *


#==============================================================================

HOST = socket.gethostbyname('0.0.0.0')#'192.168.0.24'
PORT = int(sys.argv[1])

threadCount = 0
room_list = []

room_cmd_queue = {}
room_cmd_queue_lock = threading.Lock()

#==============================================================================


def new_client(conn,addr, objR):
    global threadCount
    global room_list
    global room_cmd_queue

    # Initial msg upon contact
    INIT_MSG = str(conn.recv(BUFFER_SIZE), 'utf-8');
    
    # Handles almost all future messages
    msgHandler = MsgHandler()


    #===================================================
    # Set initial flag values to be used by master threads
    #===================================================
    stream_video = False
    streamin_frame_data = False
    triggered_active = False
    triggerable_found = False
    conn.setblocking(0) 


    #===================================================
    # If the GUI is making a request handle that
    #===================================================
    if ("GUI" in INIT_MSG):

        # Handle Basic Data requests e.g. number of rooms, names etc.
        if "GET ROOM_NAMES" in INIT_MSG:
            print("Getting room names" + ",".join(room_list))
            conn.send(str.encode(",".join(room_list) + "\n"))
        elif "GET ROOM_COUNT" in INIT_MSG:
            print("Getting room count" + threadCount)
            conn.send(str.encode(str(threadCount) + "\n"))

        # Handle SET commands to alter the flow or actions of the master
            # SET STREAM cmd opens a streaming window to view live activity
        elif "GET STREAM" in INIT_MSG:
            with room_cmd_queue_lock:
                ROOM_NAME = INIT_MSG.split("GET STREAM ")[1][:-1]
                print("Streaming : " + ROOM_NAME)
                if ROOM_NAME in room_cmd_queue:
                    room_cmd_queue[ROOM_NAME].append(INIT_MSG) 
                else:
                    room_cmd_queue[ROOM_NAME] = [INIT_MSG] 
                    
                print(room_cmd_queue)
            conn.send(str.encode("Opening Stream.\n"))

        # Report erroneous requests, mainly for debugging/dev work.
        else:
            print ("REQUEST ERROR : ", INIT_MSG)


    #===================================================
    # Else an edge device has connected therefore keep 
    # the connection open and wait for new frame data.
    #===================================================
    else:
        ROOM_NAME = INIT_MSG
        print ("New Connection from : "+ROOM_NAME)
        
        room_list.append(ROOM_NAME)
        threadCount += 1
        frame_count = 0

        last_frame_time = time.time()
        last_trigger_time = time.time()
        
        frame = np.zeros( (960, 1280, 3), dtype=np.uint8)
        output_file_name = ""
        
        # Continually check for new messages
        while True:
            next_msg = msgHandler.getNextMsg(conn)


            #===================================================
            # If there is a message, handle it yo
            #===================================================
            if next_msg:


                #===================================================
                # Handle frame data sent from edge device
                #===================================================
                if (next_msg.type != MsgType.PURE_MSG):
                    frame_count += 1 

                    # If not filming begin a new video capture
                    if not streamin_frame_data:
                        triggerable_found = False

                        streamin_frame_data = True 
                        print("Streaming Frame Data")
                   
                        now = datetime.datetime.now()
                        dateAndTime = now.strftime("%Y%m%d_%H%M%S")
                        
                        fourcc = cv2.VideoWriter_fourcc(*'avc1')
                        output_file_name = ROOM_NAME + "_" + dateAndTime + "_output.avi"
                        outputVid = cv2.VideoWriter(output_file_name,fourcc,20,(1280,960))


                    # Mark last frame time and retrieve data from message
                    last_frame_time = time.time()
                    frame = next_msg.frame_data
                    frame = cv2.resize(frame,(1280,960))

                    # Handle image recognition and results
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

                    # If we are writing to a video file write 
                    if streamin_frame_data:  
                        outputVid.write(frame)
                        outputVid.write(frame)
                #===================================================
                

                #===================================================
                # Handle Mesages sent from edge device
                #===================================================
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
                #===================================================

            #===================================================

            
            #===================================================
            # Check if transmition has timed out from no movement
            #===================================================
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
            #===================================================
            

            #===================================================
            # Check for new GUI commands to process
            #===================================================
            cmd = ""
            with room_cmd_queue_lock:

                if ROOM_NAME in room_cmd_queue:
                    cmd_list = room_cmd_queue[ROOM_NAME]
                    if len(room_cmd_queue[ROOM_NAME]) > 0:
                        cmd = room_cmd_queue[ROOM_NAME].pop()
            
            if cmd != "":
                if "STREAM" in cmd:
                    stream_video = True
            #===================================================


            #===================================================
            # Handle displaying a streamed view of the room
            #===================================================
            if stream_video:
                cv2.namedWindow(ROOM_NAME, cv2.WINDOW_NORMAL)
                cv2.imshow(ROOM_NAME,frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.destroyWindow(ROOM_NAME)
                stream_video = False
            #===================================================
        



#--------------------EXIT HANDLER-------------------
def exit_handler(s):
    print("Closing Socket and windows")
    s.close()
    cv2.destroyAllWindows()



#-------------------MAIN EXECUTION-------------------
def main():

    # Open a server side socket and handle init and close proc
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST,int(sys.argv[1])))
    s.listen(5)
    atexit.register(exit_handler, s)
   

    # IF we are performing image recognition build net
    objR = None
    if PERFORM_RECOGNITION: objR = ObjRecognition()
    

    # Begin looking for connections
    print ('Socket is now listening')
    while True:
        conn, addr = s.accept()
        _thread.start_new_thread(new_client,(conn,addr, objR));



if __name__ == "__main__" : main()
