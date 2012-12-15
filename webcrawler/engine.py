from linkfinder.linkfinder import LinkFinder
from database.database import Database
from threading import Thread

maxentries = 10000
die = [False]

def start_engine():
	database = Database()
	size = database.getSize()
	while size <= maxentries:
		size = database.getSize()
		print 'Rows in database: ' + str(size)
		url = database.getUnvisited()
		if url is None:
			break
		finder = LinkFinder(url)
		if finder.isOkay():
			database.update(url)
			linklist = finder.getLinks()
			print 'Links found: ' + str(len(linklist))
			for link in linklist:
				if len(link) > 255:
					linklist.remove(link)
			database.addNew(linklist)
		else:
			database.markBAD(url)
			print 'Marked link as bad, reason: ' + finder.reason()
		finder.close()
		if die[0]:
			break
	database.close()

def command_line(ref):
	raw_input('Hit any key to kill...')
	ref[0] = True

if __name__ == '__main__':
	print 'web crawler is now running...'
	user_thread = Thread(target=command_line, args=(die,))
	user_thread.daemon = True
	user_thread.start()
	start_engine()
	print 'web crawler is now terminating...'

