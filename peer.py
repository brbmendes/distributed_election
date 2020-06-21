# Alunos: 		
# Trabalho 2:	Eleição Distribuída - Algoritmo do Valentão (Bully Algorithm)
# Disciplina:	Programação Distribuída 

from flask import Flask
from flask_restful import Api, Resource, reqparse
import sys,threading,time,requests

app = Flask(__name__)
api = Api(app)

class Status(Resource):
	# Get is used to check node status
	def get(self):
		global me
		if me.isActive:
			return "OK", 200
		else:
			return "NOK", 200
		

	# Put is used to run election
	def put(self):
		return "PUT OK", 201
	
	# Post is used to tell everyone who is the new coordinator
	def post(self):
		return "POST OK", 201

# Node info
class Node:
	def __init__(self,id,host,port,isActive,timer,greatherNodes,lesserNodes):
		self.id = id
		self.host = host
		self.port = port
		self.isActive = isActive
		self.isCoordinator = False
		self.timer = timer
		self.greatherNodes = greatherNodes
		self.lesserNodes = lesserNodes

# Thread to run flask
class RunFlask:
	def __init__(self, app,myIp,myPort):
		thread = threading.Thread(target=self.run, args=(app,myIp,myPort))
		thread.daemon = True
		thread.start()

	def run(self,app,myIp,myPort):
		app.run(host=myIp, port=myPort, debug=False, use_reloader=False)   

# Thread to control if node is alive or dead
class StartCountTimeAlive:
	def __init__(self):
		thread = threading.Thread(target=self.run, args=())
		thread.daemon = True
		thread.start()

	def run(self):
		global me
		while True:
			if(me.isCoordinator):
				while me.timer > 0:
					me.timer -= 1
					print(me.timer)
					if(me.timer <= 0):
						me.isActive = False
						me.isCoordinator = False
					time.sleep(1)
			time.sleep(1)

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
	node = Node(int(splittedInfo[0]),splittedInfo[1],splittedInfo[2],False,10,[],[])
	if(myId > int(splittedInfo[0])):
		me.lesserNodes.append(node)
	else:
		me.greatherNodes.append(node)

# Run webservice in separated thread to receive messages
#example=RunFlask(app,myIp,myPort)
flask = RunFlask(app,myIp,myPort)

# While all nodes are not online
while not canStart:
	# Check if greather nodes are online
	for i in me.greatherNodes:
		if not i.isActive:
			try:
				# If node is online, and send back response
				httpRead = requests.get("http://"+ i.host +":"+ i.port +"/status/")
				readedValue = httpRead.text.replace("\"","")
				# Set node as active
				# print("id do nodo ativo:",readedValue)
				i.isActive = True
				# Append node on active nodes list
				activeNodes.append(i)
			except:
				None
				# print("Host {}, port {} offline".format(i.host, i.port))
	
	# Check if lesser nodes are online
	for i in me.lesserNodes:
		if not i.isActive:
			try:
				# If node is online, and send back response
				httpRead = requests.get("http://"+ i.host +":"+ i.port +"/status/")
				readedValue = httpRead.text.replace("\"","")
				# Set node as active
				# print("id do nodo ativo:",readedValue)
				i.isActive = True
				# Append node on active nodes list
				activeNodes.append(i)
			except:
				None
				# print("Host {}, port {} offline".format(i.host, i.port))

	if len(activeNodes) == int(qtdNodes):
		canStart = True
	
	time.sleep(1)

print("starting")
# Sort active nodes to get coordinator
activeNodes.sort(key=lambda x: x.id, reverse=True)

# Set coordinator as the greather id of nodes
coordinator = activeNodes[0]
if(coordinator.id == me.id):
	me.isCoordinator = True

# start counting my time alive
nodealive = StartCountTimeAlive()

# At this point, we know de coordinator ID
while(len(activeNodes) > 0):
	try:
		if(not me.isCoordinator):
			httpRead = requests.get("http://"+ coordinator.host +":"+ coordinator.port +"/status/")
			readedValue = httpRead.text.replace("\"","")
			print(readedValue)
			# Receive NOK, node is dead...
			if(readedValue == "NOK"):
				# remove coordinator from active nodes
				activeNodes.pop(0)
				print("coordinator is dead")
				break
				# start election
				# set new coordinator
				None
			else:
				print("Received {} from coordinator ID {}".format(readedValue, coordinator.id))
	except:
		None
	
	time.sleep(3)


print("End of Program")