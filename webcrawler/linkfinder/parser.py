from HTMLParser import HTMLParser
from urlparse import urlsplit
from urlparse import urljoin
from urlparse import urldefrag
import re

class Parser(HTMLParser):
	rootname = ''
	linklist = []
	encoding = None

	def __init__(self, rootname, encoding):
		HTMLParser.__init__(self)
		self.rootname = rootname
		self.encoding = encoding

	def handle_starttag(self, tag, attrs):
		if tag == 'a':
			for attr in attrs:
				if attr[0] == 'href':
					clean(self.rootname, attr[1], self.linklist)
	
	def feed(self, data):
		try:
			if self.encoding is not None:
				data = data.decode(self.encoding)
			HTMLParser.feed(self, data)
		except UnicodeDecodeError:
			print 'BADSEED!'
			print self.encoding
			print self.rootname

def clean(rootname, toclean, outlist):
	urlob = urlsplit(toclean, scheme='http')
	if urlob.netloc == '':
		try:
			toclean = urljoin(rootname, toclean)
			urlob = urlsplit(toclean)
		except AttributeError:
			return
	toclean = urldefrag(urlob.geturl())[0]
	if toclean != rootname and toclean != rootname + '/':
		outlist.append(toclean)

