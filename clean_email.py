import os, re, time
from pyner import Pyner
# STEP 1 - Clean up useless headers (Takes the message as a string)
def cleanHeaders(text, full=False): 
	f = open('clean.tmp','w')
	f.write(text)
	f.close()
	if not full:
		pmsg = os.popen('perl -ne \'if (/^\s*$/) {$b=1;} print if (/^(Subject|Reply-To|To|From):/||$b);\' clean.tmp')
	else:
		pmsg = os.popen('perl -ne \'if (/^\s*$/) {$b=1;} print if (/^(qwertyu12):/||$b);\' clean.tmp')
	message = pmsg.read()
	pmsg.close()
	os.remove('clean.tmp')
	return message

# STEP 2 - Extract useful headers. (Takes the message as a string)
def extractHeaders(text):
	mailsrch = re.compile(r'[\w\-][\w\-\.]+@[\w\-][\w\-\.]+[a-zA-Z]{1,4}')
	msg_lines = text.split('\r\n')
	headers = {'Reply-To': None, 'From': None, 'To': None, 'Subject': None}
	for line in msg_lines:
		for header in headers:
			if header in line and headers[header] == None:
				if line.strip().index(header) < 2:
					if header == 'Subject':
						headers[header] = line.replace('Subject','')
						headers[header] = headers[header].replace(': ','')
					else:
						regexp = mailsrch.findall(line)
						if regexp:
							headers[header] = regexp[0]
	return headers
#	return [(k, v) for k, v in headers.iteritems()]

# STEP 3 - Remove all headers. (Takes the message as a string)
def removeHeaders(text):
	return cleanHeaders(text, full=True)

# STEP 4 - Named Entity Recognition (Takes the message as a string)
def extractNames(text):
	f = open('ner.tmp','w')
	f.write(text)
	f.close()
	ner = Pyner()
	result = ner.getNames('ner.tmp')
	os.remove('ner.tmp')
	return result

# STEP 5 - Get all email addresses from the body of the text
def extractEmails(text):
	mailsrch = re.compile(r'[\w\-][\w\-\.]+@[\w\-][\w\-\.]+[a-zA-Z]{1,4}') # extract all email addresses
	return list(set(mailsrch.findall(text)))

# STEP 6 - Relate email addresses from body to people
def getBigrams(string):
	s = string.lower()
	return [s[i:i+2] for i in xrange(len(s) - 1)]

def stringSim(str1, str2):
	pairs1 = getBigrams(str1)
	pairs2 = getBigrams(str2)
	union  = len(pairs1) + len(pairs2)
	hit_count = 0
	for x in pairs1:
		for y in pairs2:
			if x == y: hit_count += 1
	return (2.0 * hit_count) / union

def rankSim(email_addr, name):
	name_var = [''.join(name.split())]
	name_var.extend(name.split())
	name_var = filter(lambda x: len(x) > 1, name_var)
	email_var = email_addr.split('@')[0]
	email_var = filter(lambda x: x.isalpha(), email_var)
	return max([stringSim(n, email_var) for n in name_var]) 

def computeRanking(names, email_addrs):
	ranking = {}
	email_addrs = [x.lower() for x in email_addrs]
	for email_addr in email_addrs:
		for name in names:
			score = rankSim(email_addr, name)
			if email_addr in ranking:
				if score > ranking[email_addr][1]:
					ranking[email_addr] = (name, score)
			else:
				ranking[email_addr] = (name, score)						
	return ranking

def proximitySearch(name, text):
	text = text.split('\r\n')
	text = filter(None, text)
	mailsrch = re.compile(r'[\w\-][\w\-\.]+@[\w\-][\w\-\.]+[a-zA-Z]{1,4}')
	for i in range(0, len(text)):
		if name in text[i]:
			if mailsrch.findall(text[i]):
				return (mailsrch.findall(text[i])[0].lower(), 0)
			if i + 1 < len(text):
				if mailsrch.findall(text[i+1]):
					return (mailsrch.findall(text[i+1])[0].lower(), 1)
			if i > 0:
				if mailsrch.findall(text[i-1]):
					return (mailsrch.findall(text[i-1])[0].lower(), 1)
			if i + 2 < len(text):
				if mailsrch.findall(text[i+2]):
					return (mailsrch.findall(text[i+2])[0].lower(), 2)
			if i > 1:
				if mailsrch.findall(text[i-2]):
					return (mailsrch.findall(text[i-2])[0].lower(), 2)
	return None

def relateEntities(names, emails, text):
	emails = [x.lower() for x in emails]
	relations = {}
	rankings = computeRanking(names, emails)
	for entity in rankings:
		if rankings[entity][1] > 0.4:
			relations[entity] = rankings[entity][0]
	if relations.values():
		rels_values = [x[0].lower() for x in relations.values()]
	else:
		rels_values = []
	rels_keys = [x.lower() for x in relations.keys()]
	names = filter(lambda x: x.lower() not in rels_values, names)
	emails = filter(lambda x: x.lower() not in rels_keys, emails)
	proximity_scores = {}
	if emails:
		for name in names:
			email_score = proximitySearch(name, text)
			if email_score and email_score[0].lower() not in rels_keys:
				email_addr, score = email_score[0], email_score[1]
				if email_addr in proximity_scores:
					if score < proximity_scores[email_addr][1]: #looking for minimal score
						proximity_scores[email_addr] = (name, score)
				else:
					proximity_scores[email_addr] = (name, score)
	for email_addr in proximity_scores:
		relations[email_addr] = proximity_scores[email_addr][0]
	return relations
	
# STEP 7 Something to piece the puzzle all together....
def extractInfo(text):
	messages = []
	date = time.ctime()
	text = cleanHeaders(text)
	headers = extractHeaders(text)
	text = removeHeaders(text)
	names = extractNames(text)
	unassoc_names = names
	emails = extractEmails(text)
	relations = relateEntities(names, emails, text)
	for email in relations:
		emails = filter(lambda x: x != email, emails)
		unassoc_names = filter(lambda x: x != relations[email], unassoc_names)
		msg = dict()
		msg['Date'], msg['Reply-To'], msg['To'], msg['Subject'], msg['Body'], msg['First_name'], msg['Last_name'] = date, email, headers['To'], headers['Subject'], text, " ".join(relations[email].split()[:-1]), relations[email].split()[-1]
		messages.append(msg)
	email_addr = None
	for email in emails:
		if email in headers['Reply-To']:
			email_addr = email
		if email in headers['From'] and not email_addr:
			email_addr = email
	if email_addr:
		if unassoc_names and names:
			if unassoc_names[-1] == names[-1]:
				msg = dict()
				msg['Date'], msg['Reply-To'], msg['To'], msg['Subject'], msg['Body'], msg['First_name'], msg['Last_name'] = date, email, headers['To'], headers['Subject'], text, " ".join(names[-1].split()[:-1]), names[-1].split()[-1]
				messages.append(msg)
			else:
				msg['Date'], msg['Reply-To'], msg['To'], msg['Subject'], msg['Body'], msg['First_name'], msg['Last_name'] = date, email, headers['To'], headers['Subject'], text, None, None
				messages.append(msg)
	return messages

def prettyPrint(text):
	messages = extractInfo(text)
	for msg in messages:
		print "\r\n"
		print "Date:", msg['Date']
		print "Reply-To:", msg['Reply-To']
		print "To:", msg['To']
		print "Subject:", msg['Subject']
		print "Name:", " ".join([msg['First_name'], msg['Last_name']])
		print "Body:"
		print msg['Body']
	return