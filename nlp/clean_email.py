import os, re, time
# Takes a large string - STEP 1
def stripHeaders(email): 
	f = open('clean.tmp','w')
	f.write(email)
	f.close()
	time.sleep(1)
	print os.popen('pwd').read()
	pmsg = os.popen('perl -ne \'if (/^\s*$/) {$b=1;} print if (/^(Subject|Reply-To|To|From):/||$b);\' clean.tmp')
	message = pmsg.read()
	pmsg.close()
	os.remove('clean.tmp')
	return message

# STEP 2 - Named Entity Recognition
# TODO

# STEP 3 - Get emails & relate them to entities -> The generic email finder should be in a class.
# TODO 
def getEmails(text): # takes a list of strings - STEP 2. 
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

