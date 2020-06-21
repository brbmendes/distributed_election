# Alunos: 		Bruno Mendes, Ezequiel Rinco e xxx
# Trabalho 2:	Eleição Distribuída - Algoritmo do Valentão (Bully Algorithm)
# Disciplina:	Programação Distribuída 

from flask import Flask
from flask_restful import Api, Resource, reqparse
import sys,threading,time,requests

app = Flask(__name__)
api = Api(app)

class Status(Resource):
	def get(self):
		global me
		return str(me.id), 200

	# Put é usado para avisar que outro nodo esta ativo
	def put(self):
		return "PUT OK", 201
	
	# Post é usado para aviasr que é o novo coordenador
	def post(self):
		return "POST OK", 201

class Node:
	def __init__(self,id,host,port,isActive,timer,greatherNodes,lesserNodes):
		self.id = id
		self.host = host
		self.port = port
		self.isActive = isActive
		self.timer = timer
		self.greatherNodes = greatherNodes
		self.lesserNodes = lesserNodes

class RunFlask:
	def __init__(self, app,myIp,myPort):
		thread = threading.Thread(target=self.run, args=(app,myIp,myPort))
		thread.daemon = True
		thread.start()

	def run(self,app,myIp,myPort):
		app.run(host=myIp, port=myPort, debug=False, use_reloader=False)   


api.add_resource(Status, "/status/")

# Basic info about program
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
me = Node(myId,myIp,myPort,True,10,[],[])

# Add my node to lists
activeNodes.append(me)

# Remove my line from array
lines.pop(line-1)

# Create other nodes, define nodes greather than me and lesser than me
for i in lines:
	splittedInfo = i.split(" ")
	node = Node(splittedInfo[0],splittedInfo[1],splittedInfo[2],True,10,[],[])
	if(myId > int(splittedInfo[0])):
		me.lesserNodes.append(node)
	else:
		me.greatherNodes.append(node)

# Define me as coordinator
coordinator = me

# Run webservice in separated thread to receive messages
example=RunFlask(app,myIp,myPort)


count = 0
while not canStart:
	# Check if greather nodes are online
	for i in me.greatherNodes:
		if not i.isActive:
			try:
				# If node is online, and send back response
				httpRead = requests.get("http://"+ i.host +":"+ i.port +"/status/")
				readedValue = httpRead.text.replace("\"","")
				# Set node as active
				print("id do nodo ativo:",readedValue)
				i.isActive = True
				# Append node on active nodes list
				activeNodes.append(i)
			except:
				print("Host offline:",i.host)
	
	# Check if lesser nodes are online
	for i in me.lesserNodes:
		if not i.isActive:
			try:
				# If node is online, and send back response
				httpRead = requests.get("http://"+ i.host +":"+ i.port +"/status/")
				readedValue = httpRead.text.replace("\"","")
				# Set node as active
				print("id do nodo ativo:",readedValue)
				i.isActive = True
				# Append node on active nodes list
				activeNodes.append(i)
			except:
				print("Host offline:",i.host)

	if len(activeNodes) == qtdNodes:
		canStart = True

activeNodes.sort(key=lambda x: x.id, reverse=True)

coordinator = activeNodes[0]

print("encerrou sem conectar")
