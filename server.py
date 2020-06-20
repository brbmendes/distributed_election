#!/usr/bin/env python

import socket,sys

BUFFER_SIZE = 20  # Normally 1024, but we want fast response

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

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((str(myIp), myPort))
s.listen(1)

conn, addr = s.accept()
print ('Connection address:', addr)
while 1:
    data = conn.recv(BUFFER_SIZE)
    if not data:
        print(".")
    else:
        text = date.decode()
        if (text == "exit"):
            break
        else:
            print ("received:", data)
            data = str.encode("devolvido")
            conn.send(data)  # echo
conn.close()
