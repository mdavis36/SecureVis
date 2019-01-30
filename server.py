#/usr/bin/python

import socket
import cv2
import pickle
import numpy as np
import struct
import sys

HOST ='127.0.0.1'
PORT = 1110
BUFFER_SIZE = 4096
STRUCT_ARG = "L"

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((HOST,PORT))
s.listen(10)
print 'Socket is now listening'

conn, addr = s.accept()

data = ""
# Packet will be the size of largest unsigned LONG value
packet_size = struct.calcsize(STRUCT_ARG);

while True:
    while len(data) < packet_size:
        data += conn.recv(BUFFER_SIZE)
    packed_msg_size = data[:packet_size]
    data = data[packet_size:]
    msg_size = struct.unpack(STRUCT_ARG,packed_msg_size)[0]
    while len(data) < msg_size:
        data += conn.recv(BUFFER_SIZE)
    raw_frame = data[:msg_size]
    data = data[msg_size:]

    frame = pickle.loads(raw_frame)
    print frame
    cv2.imshow('frame',frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()


