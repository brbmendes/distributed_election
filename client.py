#!/usr/bin/env python

import socket,sys

BUFFER_SIZE = 1024  # Normally 1024, but we want fast response

line = int(sys.argv[2])

f = open("arquivo_config.txt", "r")
lines = f.read().splitlines()
f.close()

myInfo = lines[line-1]
splittedInfo = myInfo.split(" ")
myId = int(splittedInfo[0])
myIp = splittedInfo[1]
myPort = int(splittedInfo[2])
print(myId)
print(myIp)
print(myPort)

destInfo = lines[0]
destSplittedInfo = myInfo.split(" ")
destId = int(destSplittedInfo[0])
destIp = destSplittedInfo[1]
destPort = int(destSplittedInfo[2])

while 1:
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print("socket created")
	
	s.connect((destIp, destPort))
	print("socket connected")
	
	message = input('digite algo: ')
	print(message)
	bytemessage = str.encode(message)
	print("encoded")
	
	s.send(bytemessage)
	print("sended")

	data = s.recv(BUFFER_SIZE)
	print("received")
	
	s.close()
	print("closed")

	print ("received data:", data)

