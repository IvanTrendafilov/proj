import os, re, time
from pyner import Pyner
# STEP 1 - Clean up the headers. (Takes the message as a string)
def stripHeaders(email): 
	f = open('clean.tmp','w')
	f.write(email)
	f.close()
	time.sleep(1)
	pmsg = os.popen('perl -ne \'if (/^\s*$/) {$b=1;} print if (/^(Subject|Date|Reply-To|To|From):/||$b);\' clean.tmp')
	message = pmsg.read()
	pmsg.close()
	os.remove('clean.tmp')
	return message

# STEP 2 - Named Entity Recognition (Takes the message as a string)
def recognize(email):
	f = open('ner.tmp','w')
	f.write(email)
	f.close()
	ner = Pyner()
	result = ner.getNames('ner.tmp')
	os.remove('ner.tmp')
	return result

# STEP 3 - Email extraction 
def getEmails(email, names):
	result = []
	mailsrch = re.compile(r'[\w\-][\w\-\.]+@[\w\-][\w\-\.]+[a-zA-Z]{1,4}') # extract all email addresses
	email_addr = mailsrch.findall(email)
	msg_lines = email.split('\r\n')
	field_replyto, field_from = 0, 0
	for line in msg_lines:
		if 'Reply-To' in line:
			field_replyto = mailsrch.findall(line)[0]
		if 'From:' in line:
			field_from = mailsrch.findall(line)[0]
	if field_replyto == None and field_from != None:
		result.append(names[-1], field_from, 'Reply-To')
	if field_replyto != None:
		result.append(names[-1], field_replyto, 'Reply-To')
	email_addr = filter (lambda x: x != field_replyto and x != field_from, email_addr)
	del names[-1]
		
	return email_addr

# NEEDS TO BE RETHINKED
def closestMatch(email_addr, name, text):
	text = text.lower()
	name = name.lower()
	email_addr = email_addr.lower()
	email_occur_index = [x.start() for x in re.finditer(email_addr, text)]
	name_occur_index = [x.start() for x in re.finditer(name, text)]
	findClose=lambda a,l:min(l,key=lambda x:abs(x-a))
	for email_occur in email_occur_index:
		print findClose(email_occur, name_occur_index)
	
	
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

# STEP 4 - Remove remaining headers
# TODO

if __name__ == "__main__":
	t1 = time.time()
	text1 = open('../data/1.txt').read()
	text1 = stripHeaders(text1)
	emails1 = getEmails(text1.split('\r\n'))
	print text1
	print emails1

