#!/usr/bin/env python

import socket,sys

BUFFER_SIZE = 1024  # Normally 1024, but we want fast response

line = int(sys.argv[2])
print(line)

f = open("arquivo_config.txt", "r")
lines = f.read().splitlines()
f.close()

for i in lines:
	print(i)

myInfo = lines[line-1]
print("\n")
print ("myInfo: ", myInfo)

splittedInfo = myInfo.split(" ")
myId = int(splittedInfo[0])
myIp = splittedInfo[1]
myPort = int(splittedInfo[2])

destInfo = lines[0]
destSplittedInfo = destInfo.split(" ")
destId = int(destSplittedInfo[0])
destIp = destSplittedInfo[1]
destPort = int(destSplittedInfo[2])

while 1:
	tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	
	dest=(str(destIp), int(destPort))

	tcp.connect(dest)
	
	message = input('digite algo: ')
	bytemessage = str.encode(message)
	
	tcp.send(bytemessage)

	data = tcp.recv(BUFFER_SIZE)
	
	tcp.close()

	print ("received data:", data)

