from parser import Parser
from urlparse import urlparse
import httplib
import re

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

	def reason(self):
		return self.response.reason

	def close(self):
		self.connection.close()

	def getLinks(self):
		headers = dict(self.response.getheaders())
		encoding = None
		if 'content-type' in headers:
			encoding = headers['content-type']
			match = re.search(r'charset=(?P<encoding>.+)$', encoding)
			encoding = match.group('encoding')
		parser = Parser(self.address.geturl(), encoding)
		parser.feed(self.response.read())
		return parser.linklist

