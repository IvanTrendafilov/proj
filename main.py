## C&C: Anti-419
import os
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
# 1. No way to remove quoted text properly so far. - FIXED (somewhat...)
# 2. No way to figure out if a new message belongs to a thread or not.
# 3. No logic to tall all shit together.
# 4. Strip html tags, if necessary. - FIXED.

1. Pick up a message from incoming/
2. Compute its hash and check it against all hashes from DB
3. Figure out origin & ID & extract the info.
4. Attach to correct thread
	1. Same thread if the email address is correct.
	2. If either the first name or the last name & the correct identity address
	3. Try to find largest overlap?
	4. Maybe introduce a thread code?



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
		data = getMetadata(options[0])
		data['Content'] = open('incoming/' + options[0], 'r').read()
		print "Removing", options[0]
#		os.remove(options[0])
		return data
	return None

def theLoop():
	while True:
		incoming_msg = getMessage()
		if incoming_msg:
			msg_id, origin, content = incoming_msg['Msg_id'], incoming_msg['Origin'], incoming['Content']
			list_of_email_dicts = extractInfo(content)
			for elem in list_of_email_dicts:
				sendEmail()





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