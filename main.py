## C&C: Anti-419
import os
import time
from identity import getRandomIdentity
from responder import sendEmail
from clean_email import extractInfo
from email_classifier import classify
from dbconn import dbconn

# Filename pattern: ORIGIN-ID[-email_id].ready
# Known origins:
# COLLECTOR
# IDENTITY
# CRAWLER

# Problems
# 1. Redesign DB and persistance.
# 2. No way to figure out if a new message belongs to a thread or not. - buckets

'''
1. Pick up a message from incoming/
2. Compute its hash and check it against all hashes from DB
3. Figure out origin & ID & extract the info.
4. Attach to correct thread
	0. Email buckets
	1. Same thread if the email address is correct.
	2. If either the first name or the last name & the correct identity address
	3. Try to find largest overlap (minus stopwords), but how?
	4. Maybe introduce a thread code?
5. Send Email
6. Increment state ? Update conversation info.
7.'''
# Consider pickling stuff


def getMetadata(file_name):
	origin = file_name.split('.')[0].split('-')[0]
	msg_id = file_name.split('.')[0].split('-')[1]
	email_id = None
	if origin.lower() == 'identity':
		email_id = file_name.split('.')[0].split('-')[2]
	unique_id = origin[0].upper() + str(msg_id)
	return {'Origin': origin, 'Msg_id': unique_id, 'Email_id': email_id}

def getMessage():
	options = filter(lambda x: '.ready' in x and '~' not in x, os.listdir('incoming/'))
	if options:
		incoming_dir = 'incoming/'
		data = getMetadata(options[0])
		data['Content'] = open(incoming_dir + options[0], 'r').read()
#		os.rename(incoming_dir + options[0], incoming_dir + options[0].replace('ready','done'))
		return data
	return None

def theLoop():
	while True:
		current_msg = getMessage()
		if current_msg:
			msg_id, origin, content = current_msg['Msg_id'], current_msg['Origin'], current_msg['Content']
			identity = getRandomIdentity()
			list_of_email_dicts = extractInfo(current_msg['Content'])
			for elem in list_of_email_dicts:
				email_class = classify(elem['Body']).values()[0]
				sendEmail(elem['Body'], email_class, identity, elem, 0)
		else:
			print "Nothing..."
#		time.sleep(5)
		break
	return

    # Read a message
    # See if it is a new entry or a an existing message by checking identity
    # See if it is quoted?
    # Assign identity
    # Send email
    # How do I update?
	## Read the directory with messages
	## Check if they exist
	## If they don't exist, assign them an identity
	## Do information extraction
	## Do email classification
	## compose response
	## repy
	## update the dbconn