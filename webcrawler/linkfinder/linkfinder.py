from parser import Parser
import httplib

class LinkFinder:
	address = ''
	connection = None
	response = None

	def __init__(self, address):
		self.address = address
		self.connection = httplib.HTTPConnection(self.address, 80)
		self.connection.request('GET', '')
		self.response = self.connection.getresponse()

	def isOkay(self):
		return self.response.status == 200

	def close(self):
		self.connection.close()

	def getLinks(self):
		parser = Parser(self.address)
		parser.feed(self.response.read())
		return parser.linklist

