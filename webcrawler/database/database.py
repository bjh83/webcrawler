import MySQLdb
import datetime

class Database:
	database = None
	cursor = None

	def __init__(self):
		self.database = MySQLdb.connect(host='localhost', user='brendan', db='webcrawler')
		self.cursor = self.database.cursor()

	def getUnvisited(self):
		self.cursor.execute("""SELECT url FROM urls WHERE visited IS NULL LIMIT 1""")
		retval = self.cursor.fetchall()
		if len(retval) < 1 or len(retval[0]) < 1:
			return None
		else:
			return retval[0][0]

	def update(self, url):
		time = datetime.date.today().strftime('%Y-%m-%d')
		self.cursor.execute("""UPDATE urls SET visited='""" + time + """' WHERE url=%s""", url)

	def getSize(self):
		self.cursor.execute("""SELECT COUNT(*) FROM urls""")
		return self.cursor.fetchall()[0][0]

	def addNew(self, newLinks):
		newLinks = list(set(newLinks))
		varstring = ''
		index = 1
		while index < len(newLinks):
			varstring += '(%s), '
			index += 1
		varstring += '(%s)'
		querystring = """INSERT INTO urls (url) VALUES %s""" % varstring
		print querystring
		self.cursor.execute(querystring, newLinks)

	def remove(self, url):
		self.cursor.execute("""DELETE FROM urls WHERE url=?""", url)

	def close(self):
		self.cursor.close()

