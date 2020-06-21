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

class ThreadingExample(object):
	def __init__(self, interval=1):
		""" Constructor
		:type interval: int
		:param interval: Check interval, in seconds
		"""
		self.interval = interval

		thread = threading.Thread(target=self.run, args=())
		thread.daemon = True
		thread.start()

	def run(self):
		""" Method that runs forever """
		while True:
			# Do something
			print('.', end="")

			time.sleep(self.interval)    

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

example=ThreadingExample()

app.run(host=myIp, port=myPort, debug=True, use_reloader=False)