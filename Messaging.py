#/usr/bin/python
from enum import Enum
from Const import *
import struct
import pickle
import socket


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


        while len(self.data) < msg_size:
           self.data += conn.recv(BUFFER_SIZE)
        

        raw_frame = self.data[:msg_size]
        self.data = self.data[msg_size:]
   

        if (msg_size > 32): msg_type = MsgType.MOTION_FRAME
        else: msg_type = MsgType.PURE_MSG


        return Message(raw_frame, msg_size, msg_type)




