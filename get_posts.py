from BeautifulSoup import BeautifulSoup
import urllib2
import os


def findLimit():
	core_url = "http://forum.419eater.com/forum/"
	page_name = "viewforum.php"
	forum_args = "?f=18&start="
	page_increment = 0
	while True:
		try:
			current_page = urllib2.urlopen(core_url + page_name + forum_args + str(page_increment))
		except:
			pass  # fail silently
		soup = BeautifulSoup(current_page)
		count = 0
		for link in soup.findAll('a', href=True):
			if 'viewtopic.php' in link['href']:
				if count > 7:
					break
				count += 1
		if count == 7:
			break
		page_increment += 30
	return page_increment - 30  # adjust for final, empty page


def crawlIndex(limit=270):
	links = []
	exceptions = ['188427', '105921', '190170', '176248']  # administrative topics
	core_url = "http://forum.419eater.com/forum/"
	page_name = "viewforum.php"
	forum_args = "?f=18&start="
	page_increment = 0
	while page_increment <= limit:
		try:
			current_page = urllib2.urlopen(core_url + page_name + forum_args + str(page_increment))
		except:
			print "Failing on:", core_url + page_name + forum_args + str(page_increment)
		soup = BeautifulSoup(current_page)
		for link in soup.findAll('a', href=True):
			if 'viewtopic.php' in link['href']:
				try:
					link_id = link['href'].split('&')[0].split('=')[1]
					if link_id not in links and str(link_id) not in exceptions:
						links.append(str(link_id))
				except:
					print "Problem in link separation"
		page_increment += 30
	return list(set(links) - set(exceptions))


def crawlPost(link_id):
	exceptions = ['ipTRACKERonline.com']
	core_url = "http://forum.419eater.com/forum/"
	page_name = "viewtopic.php"
	forum_args = "?t="
	response = None
	try:
		post = urllib2.urlopen(core_url + page_name + forum_args + link_id)
		soup = BeautifulSoup(post, convertEntities=BeautifulSoup.HTML_ENTITIES)
		try:  # hating BeautifulSoup
			response = soup.findAll("td", {"class": "postbody"})[1]
			response = response.renderContents()
			for elem in exceptions:
				if elem in response:
					return None
			response = response.replace('<br />\n<br />\n', '<magic>\n')
			response = response.replace('<br />\n', '')
			response = response.replace('<magic>\n', '<br />\n')
			response = BeautifulSoup(response)
			response = response.findAll(text=True)
			response = ''.join(response)
			response = response.encode('ascii', 'ignore')
			response = response.replace('\r\n ', '\r\n')
			response = response.replace('\n\n  Quote:   ', '')
		except:
			return None
	except:
		print "Failing on:", core_url + page_name + forum_args + link_id
	return response  # WARNING: Unicode


def crawlAndWrite(links):
	for link_id in links:
		response = crawlPost(link_id)
		if response:
			filename = os.environ['HOME'] + 'dev/proj/data/test/' + link_id + '.txt'
			fileh = open(filename, 'w')
			fileh.write(response)
	return


def go():
	crawlAndWrite(crawlIndex(findLimit()))
	return
