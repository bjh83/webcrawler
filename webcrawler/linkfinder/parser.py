from HTMLParser import HTMLParser
import re

class Parser(HTMLParser):
	rootname = ''
	linklist = []

	def __init__(self, rootname):
		HTMLParser.__init__(self)
		self.rootname = rootname

	def handle_starttag(self, tag, attrs):
		if tag == 'a':
			for attr in attrs:
				if attr[0] == 'href':
					clean(self.rootname, attr[1], self.linklist)

def clean(rootname, toclean, outlist):
	if re.match(r'/\w+', toclean) is not None:
		toclean = rootname + toclean
	if re.match(r'\w+/', toclean) is not None:
		toclean = rootname + toclean
	m = re.match(r'http://', toclean) 
	if m is not None:
		toclean = toclean[m.end():]
	if toclean != rootname and toclean != '' and re.match(r'\w', toclean) is not None:
		outlist.append(toclean)

