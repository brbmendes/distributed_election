# Alunos: 		Bruno Mendes, Ezequiel Rinco e xxx
# Trabalho 2:	Eleição Distribuída - Algoritmo do Valentão (Bully Algorithm)
# Disciplina:	Programação Distribuída 

from flask import Flask
from flask_restful import Api, Resource, reqparse
import sys,threading,time

app = Flask(__name__)
api = Api(app)

class Status(Resource):
	def get(self):
		global me
		msg = "meu id eh" + me.id
		return msg, 200

	def put(self):
		return "PUT OK", 201
	
	def post(self):
		return "POST OK", 201

class Node:
	def __init__(self,id,host,port,isCoordinator,isActive,timer,greatherNodes,lesserNodes,counterActives):
		self.id = id
		self.host = host
		self.port = port
		self.isCoordinator = isCoordinator
		self.isActive = isActive
		self.timer = timer
		self.greatherNodes = greatherNodes
		self.lesserNodes = lesserNodes
		self.counterActives = counterActives

class RunFlask:
	def __init__(self, app,myIp,myPort):
		thread = threading.Thread(target=self.run, args=(app,myIp,myPort))
		thread.daemon = True
		thread.start()

	def run(self,app,myIp,myPort):
		app.run(host=myIp, port=myPort, debug=True, use_reloader=False)   


api.add_resource(Status, "/status/")

coordinator = None
activeNodes = []
canStart = False
qtdNodes = 0

# Get my line
line = int(sys.argv[2])

# Open and read all lines
# Split into array "lines"
f = open(sys.argv[1], "r")
lines = f.read().splitlines()
f.close()

# Set number of all nodes
qtdNodes = len(lines)

# Get my info
info = lines[line-1]
splittedInfo = info.split(" ")
myId = int(splittedInfo[0])
myIp = splittedInfo[1]
myPort = splittedInfo[2]

# Create my node
me = Node(myId,myIp,myPort,False,True,10,[],[],1)

# Add my node to lists
activeNodes.append(me)

# Remove my line from array
lines.pop(line-1)

# Create other nodes, define nodes greather than me and lesser than me
for i in lines:
	splittedInfo = i.split(" ")
	node = Node(splittedInfo[0],splittedInfo[1],splittedInfo[2],False,True,10,[],[],1)
	if(myId > int(splittedInfo[0])):
		me.lesserNodes.append(node)
	else:
		me.greatherNodes.append(node)


example=RunFlask(app,myIp,myPort)



print("meu id:", me.id)

while 1:
	print("eita")
	time.sleep(3)
