# Alunos: 		Bruno Mendes e Ezequiel Rinco
# Estratégia: 	Algoritmo Centralizado

from flask import Flask
from flask_restful import Api, Resource, reqparse
import sys,threading,time

app = Flask(__name__)
api = Api(app)

class Operation(Resource):
	def get(self):
		return "GET OK", 200

	def put(self):
		return "PUT OK", 201
	
	def post(self):
		return "POST OK", 201

class Node:
	def __init__(self,id,host,port,isCoordinator,isActive,timer,greatherNodes,counterActives):
		self.id = id
		self.host = host
		self.port = port
		self.isCoordinator = isCoordinator
		self.isActive = isActive
		self.timer = timer
		self.greatherNodes = greatherNodes
		self.counterActives = counterActives

class Run_Flask:
	def __init__(self, app,myIp,myPort):
		thread = threading.Thread(target=self.run, args=(app,myIp,myPort))
		thread.daemon = True
		thread.start()

	def run(self,app,myIp,myPort):
		app.run(host=myIp, port=myPort, debug=True, use_reloader=False)   

api.add_resource(Operation, "/operation/")

line = int(sys.argv[2])

f = open(sys.argv[1], "r")
lines = f.read().splitlines()
f.close()

myInfo = lines[line-1]

splittedInfo = myInfo.split(" ")
myId = int(splittedInfo[0])
myIp = splittedInfo[1]
myPort = splittedInfo[2]

print(myIp)
print(myPort)

example=ThreadingExample(app,myIp,myPort)

node1 = Node(myId,myIp,myPort,False,True,10,[],1)

print("meu id:", node1.id)

while 1:
	print("eita")
	time.sleep(3)
