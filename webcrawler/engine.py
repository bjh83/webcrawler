from linkfinder.linkfinder import LinkFinder
from database.database import Database
from threading import Thread
import sys
import socket

maxentries = 10000
die = [False]

def start_engine():
	database = Database()
	size = database.getSize()
	while size <= maxentries:
		size = database.getSize()
		print 'Rows in database: ' + str(size)
		url = database.getUnvisited()
		database.update(url)
		if url is None:
			break
		try:
			finder = LinkFinder(url)
			if finder.isOkay():
				linklist = finder.getLinks()
				print 'Links found: ' + str(len(linklist))
				for link in linklist:
					if len(link) > 255:
						linklist.remove(link)
				try:
					database.addNew(linklist)
				except UnicodeEncodeError:
					print 'Link encoding error'
			else:
				database.markBAD(url)
				print 'Marked link as bad, reason: ' + finder.reason()
			finder.close()
		except socket.error:
			print 'timeout error'
			database.markBAD(url)
		except LookupError:
			print 'lookup error'
		if die[0]:
			break
	database.close()

def command_line(ref):
	raw_input('Hit any key to kill...')
	ref[0] = True

if __name__ == '__main__':
	print 'web crawler is now running...'
	if len(sys.argv) > 1:
		maxentries = int(sys.argv[1])
		print maxentries
	user_thread = Thread(target=command_line, args=(die,))
	user_thread.daemon = True
	user_thread.start()
	start_engine()
	print 'web crawler is now terminating...'

