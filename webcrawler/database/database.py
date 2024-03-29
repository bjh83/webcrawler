import MySQLdb
import datetime

class Database:
	database = None
	cursor = None

	def __init__(self):
		self.database = MySQLdb.connect(host='localhost', user='brendan', db='webcrawler')
		self.cursor = self.database.cursor()

	def getUnvisited(self):
		self.cursor.execute("""SELECT url FROM urls WHERE visited IS NULL ORDER BY discovered LIMIT 1""")
		retval = self.cursor.fetchall()
		if len(retval) < 1 or len(retval[0]) < 1:
			return None
		else:
			return retval[0][0]

	def update(self, url):
		time = datetime.date.today().strftime('%Y-%m-%d')
		self.cursor.execute("""UPDATE urls SET visited='""" + time + """' WHERE url=%s""", url)
		self.database.commit()

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
		querystring = """INSERT IGNORE INTO urls (url) VALUES %s""" % varstring
		self.cursor.execute(querystring, newLinks)
		self.database.commit()

	def markBAD(self, url):
		self.cursor.execute("""UPDATE urls set BAD=1 WHERE url=%s""", url)
		self.database.commit()

	def close(self):
		self.cursor.close()

