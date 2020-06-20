#!/usr/bin/env python

import socket


TCP_IP = "10.0.2.13"
TCP_PORT = 25123
BUFFER_SIZE = 1024
MESSAGE = "Hello, World2!"
print(MESSAGE)
bytemessage = str.encode(MESSAGE)
print("encoded")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("socket created")
s.connect((TCP_IP, TCP_PORT))
print("socket connected")
s.send(bytemessage)
print("sended")
data = s.recv(BUFFER_SIZE)
print("received")
s.close()

print ("received data:", data)
