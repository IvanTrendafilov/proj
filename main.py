## C&C: Anti-419
import os
import time
import cPickle as pickle
import hashlib
from identity import getRandomIdentity, getIdentityEmails, getIdentityByID
from responder import sendEmail
from clean_email import extractInfo, removeHTML, extractEmails, getEmails, extractHeaders_safe, removeHeaders_safe, removeHeaders
from email_classifier import classify

'''
TODO:
1. Finish the implementation of stories and trigger words
2. Deal with repeating info.
3. Consider a store for unhandled emails
'''

# Filename pattern: ORIGIN-ID.ready
# Known origins:
# COLLECTOR
# IDENTITY
# CRAWLER

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

def reset():
	os.remove('data/hashes.pkl')
	os.remove('data/conv_store.pkl')
	return

def init():
	try:
		hashes_pkl = open('data/hashes.pkl', 'rb')
		hashes = pickle.load(hashes_pkl)
		hashes_pkl.close()
	except:
		hashes_pkl, hashes = None, []
	try: 
		conv_store_pkl = open('data/conv_store.pkl', 'rb')
		conv_store = pickle.load(conv_store_pkl)
		conv_store_pkl.close()

	except:
		conv_store_pkl, conv_store = None, {}
	return (hashes, conv_store)

def save(hashes, conv_store):
	try:
		hashes_pkl = open('data/hashes.pkl', 'wb')
		pickle.dump(hashes, hashes_pkl)
		hashes_pkl.flush()
		hashes_pkl.close()
	except:
		print "ERROR: Unable to pickle hashes."
	try:
		conv_store_pkl = open('data/conv_store.pkl', 'wb')
		pickle.dump(conv_store, conv_store_pkl)
		conv_store_pkl.flush()
		conv_store_pkl.close()
	except:
		print "ERROR: Unable to pickle conv_store."
	return
		
def getHash(text):
	return hashlib.sha224(filter(lambda x: x.isalpha(), text)).hexdigest()

def getMetadata(file_name):
	origin = file_name.split('.')[0].split('-')[0]
	msg_id = file_name.split('.')[0].split('-')[1]
	email_id = None
#	if origin.lower() == 'identity':
#		email_id = file_name.split('.')[0].split('-')[2]
	unique_id = origin[0].upper() + str(msg_id)
	return {'Origin': origin, 'Msg_id': unique_id, 'Email_id': email_id}

def getMessage():
	options = filter(lambda x: '.ready' in x and '~' not in x, os.listdir('incoming/'))
	if options:
		incoming_dir = 'incoming/'
		data = getMetadata(options[0])
		data['Content'] = open(incoming_dir + options[0], 'r').read()
		os.rename(incoming_dir + options[0], incoming_dir + options[0].replace('ready','done'))
		return data
	return None

def getConvIDByBucket(email_bucket, conv_store, identity_emails):
	counts = {}
	for conv_key in conv_store:
		counts[conv_key] = 0
		current_bucket = conv_store[conv_key]['Bucket']
		for addr in email_bucket:
			if (addr in current_bucket) and (addr not in identity_emails):
				counts[conv_key] += 1
	if counts.values():
		if max(counts.values()) > 0:
			return max(counts, key=counts.get)
	return None

def updateBucket(current_bucket, email_bucket, identity_emails):
	current_bucket = [email_addr.lower() for email_addr in current_bucket]
	current_bucket = filter(lambda x: x not in identity_emails and x.count('.') < 5, current_bucket)
	return list(set(current_bucket + email_bucket))

def getNextKey(diction):
		return max([value for value in diction.keys() if isinstance(value, int)]) + 1 if diction else 0

def findBouncedEmail(text, origin):
	if origin == "IDENTITY":
		new_text = removeHeaders_safe(text)
	else:
		new_text = removeHeaders(text)
	new_text = new_text.splitlines()
	for line in new_text:
		if extractEmails(line):
			return extractEmails(line)[0].lower()
	return None

def detectBounce(text, origin):
	if origin == "IDENTITY":
		headers = extractHeaders_safe(text)
		if 'mailer-daemon' in headers['From'].lower() and headers['Subject'].strip() == "Failure Notice":
			return findBouncedEmail(text, origin)
	else:
		if "Failure Notice" in text and "mailer-daemon" in text.lower() and "unable to deliver your message" in text:
			return findBouncedEmail(text, origin)
	return None

def closeThreads(conv_store, bounced_email):
	for conv_id in conv_store:
		if bounced_email in conv_store[conv_id]['Bucket']:
			conv_store[conv_id]['State'] = 'CLOSED'
	return conv_store

def theLoop():
	supported_msgs = ['lottery', 'orphans', 'mystery_shopper']
	while True:
		hashes, conv_store = init()
		msg_dict = {}
		current_msg = getMessage()
		if current_msg:
			fake_id, origin, content = current_msg['Msg_id'], current_msg['Origin'], current_msg['Content']
			bounce = detectBounce(content, origin)
			if bounce:
				conv_store = closeThreads(conv_store, bounce)
			current_bucket = getEmails(content)
			identity_emails = getIdentityEmails()
			conv_id = getConvIDByBucket(current_bucket, conv_store, identity_emails)
			print "Current bucket", current_bucket
			if conv_id != None and bounce == None and conv_store[conv_id]['State'] != 'CLOSED':
				print "Thread detected as", conv_id
				conv_store[conv_id]['Bucket'] = updateBucket(current_bucket, conv_store[conv_id]['Bucket'], identity_emails)
				identity_dict = getIdentityByID(conv_store[conv_id]['Identity_ID'])
				print identity_dict
				list_of_email_dicts = extractInfo(content, True, identity_dict)
				print list_of_email_dicts
				for email_dict in list_of_email_dicts:
					if (conv_store[conv_id]['Class'] in supported_msgs):
						conv_store[conv_id]['Messages'][getNextKey(conv_store[conv_id]['Messages'])] = {'Date': email_dict['Date'], 'Body': email_dict['Body'], 'Sender': email_dict['Reply-To'], 'Receiver': email_dict['To'], 'Subject': email_dict['Subject'], 'First_name': email_dict['First_name'], 'Last_name': email_dict['Last_name'], 'Origin': origin, 'PQ': None}
						sent_email_dict = sendEmail(email_dict['Body'], conv_store[conv_id]['Class'], identity_dict, email_dict, conv_store[conv_id]['State'] + 1)
						print "Dic", sent_email_dict
						if sent_email_dict:
							conv_store[conv_id]['Messages'][getNextKey(conv_store[conv_id]['Messages'])] = sent_email_dict
						conv_store[conv_id]['State'] += 1
			if conv_id == None and bounce == None:
				print "No bucket detected!"
				conv, conv['Messages'], conv['Class'], conv['State'], conv['PQ'] = {}, {}, '', -1, False
				conv['Bucket'] = updateBucket(current_bucket, [], identity_emails)
				conv['Identity_ID'], identity_dict = getRandomIdentity()
				list_of_email_dicts = extractInfo(current_msg['Content'])
				msg_dict, email_class = {}, None
				for email_dict in list_of_email_dicts:
					email_class = classify(email_dict['Body']).values()[0]
					hash_value = getHash(email_dict['Body'])
					if (email_class in supported_msgs) and (hash_value not in hashes):
						msg_dict[getNextKey(msg_dict)] = {'Date': email_dict['Date'], 'Body': email_dict['Body'], 'Sender': email_dict['Reply-To'], 'Receiver': email_dict['To'], 'Subject': email_dict['Subject'], 'First_name': email_dict['First_name'], 'Last_name': email_dict['Last_name'], 'Origin': origin, 'PQ': None}
						conv['State'] = 0
						sent_email_dict = sendEmail(email_dict['Body'], email_class, identity_dict, email_dict, conv['State'])
						if sent_email_dict:
							msg_dict[getNextKey(msg_dict)] = sent_email_dict
						if msg_dict[getNextKey(msg_dict) - 1]:
							hashes.append(hash_value)
					else:
						pass # Maybe record it somewhere?
				conv['Class'] = email_class
				conv['State'] = 1
				conv['Messages'] = msg_dict
				for elem in msg_dict:
					if msg_dict[elem]['PQ']:
						conv['PQ'] = True
				conv_store[getNextKey(conv_store)] = conv 
		else:
			print "Nothing..."
#		time.sleep(5)
		save(hashes, conv_store)
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