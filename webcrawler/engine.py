from linkfinder.linkfinder import LinkFinder
from database.database import Database

maxentries = 10000

def run():
	database = Database()
	while database.getSize() <= maxentries:
		url = database.getUnvisited()
		if url is None:
			break
		finder = LinkFinder(url)
		if finder.isOkay():
			database.update(url)
			database.addNew(finder.getLinks())
			finder.close()
		else:
			database.remove(url)
			finder.close()
	database.close()

if __name__ == '__main__':
	print 'web crawler is now running...'
	run()
	print 'web crawler is now terminating...'

