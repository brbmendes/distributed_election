# Alunos: 		Bruno Mendes e Ezequiel Rinco
# Estratégia: 	Algoritmo Centralizado

import json, requests, time, sys

if __name__ == '__main__':
	line = int(sys.argv[2])

	f = open(sys.argv[1], "r")
	lines = f.read().splitlines()
	f.close()

	myInfo = lines[line-1]

	splittedInfo = myInfo.split(" ")
	myId = int(splittedInfo[0])
	myIp = splittedInfo[1]
	myPort = splittedInfo[2]

	destInfo = lines[1]
	destSplittedInfo = destInfo.split(" ")
	destId = int(destSplittedInfo[0])
	destIp = destSplittedInfo[1]
	destPort = destSplittedInfo[2]

	print(myIp)
	print(myPort)

	print(destIp)
	print(destPort)

	count=0
	while True:
		if(count > 2):break
		httpRead = requests.get("http://"+ destIp +":" + destPort +"/status/")
		readedValue = httpRead.text.replace("\"","")
		print(readedValue)
		count += 1
	print("end of program")