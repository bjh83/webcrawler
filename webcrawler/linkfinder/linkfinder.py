from parser import Parser
from urlparse import urlparse
import httplib

class LinkFinder:
	address = ''
	connection = None
	response = None

	def __init__(self, address):
		self.address = urlparse(address)
		self.connection = httplib.HTTPConnection(self.address.netloc, 80)
		self.connection.request('GET', self.address.path)
		self.response = self.connection.getresponse()

	def isOkay(self):
		return self.response.status == 200

	def close(self):
		self.connection.close()

	def getLinks(self):
		parser = Parser(self.address.geturl())
		parser.feed(self.response.read())
		return parser.linklist

