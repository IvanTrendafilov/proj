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
	os.r
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
				if header == 'Subject':
					headers[header] = line.replace('Subject: ','')
				else:
					regexp = mailsrch.findall(line)
					if regexp:
						headers[header] = regexp[0]
#	return headers
	return [(k, v) for k, v in headers.iteritems()]

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
						print name, score
						proximity_scores[email_addr] = (name, score)
				else:
					proximity_scores[email_addr] = (name, score)
	for email_addr in proximity_scores:
		relations[email_addr] = proximity_scores[email_addr][0]
	return relations
	
# STEP 7 Something to piece the puzzle all together....
# purvo sa relations, koito sme extractnali, sled tova sa reply-to neshtata.
def extractInfo(orig_text):
	text = orig_text
	text = cleanHeaders(text) # this is cleaned from garbage
	headers = extractHeaders(text)
	text = removeHeaders(text) # this is stripped from all headers
	names = extractNames(text) # NER 
	emails = extractNames(text) # regexp for emails
	relations = relateEntities(names, emails, text)
	# produce a list of emails format - (date, reply_addr, rcpt_addr, msg_body, subject, reply_first_name, reply_last_name)
	return

'''
def closestMatch(email_addr, name, text):
	text = text.lower()
	name = name.lower()
	email_addr = email_addr.lower()
	email_occur_index = [x.start() for x in re.finditer(email_addr, text)]
	name_occur_index = [x.start() for x in re.finditer(name, text)]

def closestMatch(email_addr, name, text):
	text = text.lower()
	name = name.lower()
	email_addr = email_addr.lower()
	email_occur_index = [x.start() for x in re.finditer(email_addr, text)]
	name_occur_index = [x.start() for x in re.finditer(name, text)]
	findClose=lambda a,l:min(l,key=lambda x:abs(x-a))
	tmp_max = []
	for email_occur in email_occur_index:
		tmp_max.append(findClose(email_occur, name_occur_index))
	print (email_addr, name, max(tmp_max))
	
	
def getEmails(email_as_a_list, names):
	result = []
	email_as_a_list = text
	mailsrch = re.compile(r'[\w\-][\w\-\.]+@[\w\-][\w\-\.]+[a-zA-Z]{1,4}') # extract all email addresses
	other_emails, field_from, field_replyto = [], None, None
	for line in text:
		res = mailsrch.findall(line)
#		if res and res[0].split('@')[0].islower():
		if res:
			if 'From:' in line:
				field_from = res
			elif 'Reply-To' in line:
				field_replyto = res
			else:
				other_emails.append(res)
	for line in text:
		for name in names:
			if name in line:
				for email_addr in other_emails:
					if email_addr in line:
						result.append(name, email_addr, 'Other')

	return result
			

# relate them to entities -> The generic email finder should be in a class.
# TODO 
# Suberi reply-to adresa (ako sushtestvuva, ako ne - FROM) sus from
# Mahni gi ot bucket-a s NER results. Sled tva, asociirai ostanalite entities s nai-blizkiq rezultat.
def getEmails(text, ): # takes a list of strings - STEP 3. 
	mailsrch = re.compile(r'[\w\-][\w\-\.]+@[\w\-][\w\-\.]+[a-zA-Z]{1,4}')
	all_emails = []
	field_from = None
	field_replyto = None
	for line in text:
		res = mailsrch.findall(line)
		if res and res[0].split('@')[0].islower():			
			all_emails.append(res)
			if 'from' in line.lower() and len(line.split()) < 10:
				field_from = res
			if 'reply-to' in line.lower():
				field_replyto = res
	return (field_from, field_replyto, all_emails)

if __name__ == "__main__":
	t1 = time.time()
	text1 = open('../data/1.txt').read()
	text1 = stripHeaders(text1)
	emails1 = getEmails(text1.split('\r\n'))
	print text1
	print emails1
'''
