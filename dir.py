# TODO: MAJOR REFACTORING. 

from BeautifulSoup import BeautifulSoup
import urllib2, sqlite3, time
class forumparser(object):
	def __enter__(self):
		return self

	def __exit__(self):
		self.cur.close()

	def __init__(self):
		self.conn = sqlite3.connect('db')
		self.cur = self.conn.cursor()
		self.cur.execute("CREATE TABLE IF NOT EXISTS forum (id INTEGER, email TEXT, date TEXT)")
		self.core_url = "http://forum.419eater.com/forum/"
		self.forum_id = "viewforum.php?f=18"
		self.exceptions = [188427, 105921, 190170] # admin topics
		self.links = []

	def crawl(self):
		main_page = urllib2.urlopen(self.core_url + self.forum_id)
		self.cur.execute("SELECT id FROM forum")
		tmp = self.cur.fetchall()
		result = []
		for elem in tmp:
			result.append(elem[0])
		print result
		soup = BeautifulSoup(main_page) 
		for link in soup.findAll('a', href=True):
			if 'viewtopic.php' in link['href']:
				link_short = link['href'].split('&')[0]
				link_id = link_short.split('=')[1]
				if not(link_id in result or self.exceptions):
					self.links.append(link_short)
		return self.links

	def extract(self, link):
		link_id = link.split('=')[1]
		response = urllib2.urlopen(self.core_url + link)
		soup = BeautifulSoup(response)
		try:
			response = soup.findAll("td", { "class" : "postbody" })[1] # always the 2nd occurance
			response = ''.join(response.findAll(text=True))
			self.cur.execute("INSERT INTO forum VALUES (?, ?, ?)", (int(link_id), response, str(time.ctime())))			
		except IndexError:
			pass

	def go(self):
		all_links = set(self.crawl())
		print "To browse"
		print all_links
		for link in all_links:
			self.extract(link)
		self.conn.commit()
		self.cur.close()
