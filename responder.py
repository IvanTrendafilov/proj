import os
import random
from email_classifier import hasPQ
from string import Template
# identity_dict = {'Gender': 'male', 'Age': '47', 'Marriage': 'Single', 'First_name': 'Peter', 'Last_name': 'Donegan', 'Occupation':'an accountant', 'Address':'34 Cockburn Street', 'City':'Edinburgh', 'Country':'the UK', 'Postcode':'EH89LL', 'Telephone':'0742323123', 'Email':'peterdonegan64@yahoo.com'}

def preload():
	return {'Gender': 'male', 'Age': '47', 'Marriage': 'Single', 'First_name': 'Peter', 'Last_name': 'Donegan', 'Occupation':'an accountant', 'Address':'34 Cockburn Street', 'City':'Edinburgh', 'Country':'the UK', 'Postcode':'EH89LL', 'Telephone':'0742323123', 'Email':'peterdonegan64@yahoo.com'}

def getScenario(scenario_name):
	options = filter(lambda x: '.txt' in x and '~' not in x, os.listdir('scenarios/' + scenario_name + '/'))  #  love for FP
	return open('scenarios/' + scenario_name + '/' + random.choice(options)).read().strip()

def answerPQ(text, identity_dict, email_class):
	paragraph = ""
	postcode_words = ['post code', 'postcode', 'zip']
	intro = getScenario('pq_intro')
	ending = getScenario('pq_ending')
	marriage = ""
	if email_class == 'romance':
		marriage = getScenario('marriage')
	if "....." in text or "_____" in text:
		body = getScenario('pq_generic')
		paragraph = os.linesep + " ".join([intro + os.linesep, body, os.linesep + ending]) + os.linesep
	else:
		name = getScenario('name')
		occupation = getScenario('occupation')
		age = getScenario('age')
		location = getScenario('location')
		postcode = ""
		for word in postcode_words:
			if word in text.lower():
				postcode = getScenario('postcode')
				break
		contact = getScenario('contact')
		paragraph = os.linesep + " ".join([intro, name, occupation, age, marriage, location, postcode, contact, ending]) + os.linesep
	paragraph = Template(paragraph).safe_substitute(identity_dict)
	id_answer, photo_answer = "", ""
	id_words = ['passport',' id ','id card','license', 'license']
	photo_words = ['photo', 'picture of']
	for word in id_words:
		if word in text.lower():
			paragraph += os.linesep + getScenario('photo_request') + os.linesep
			return paragraph
	for word in photo_words:
		if word in text.lower():
			paragraph += os.linesep + getScenario('photo_request') + os.linesep
			return paragraph
	return paragraph

def quoteText(email_dict):
	if email_dict['Body']:
	#	prefix = os.linesep + os.linesep + "On " + email_dict['Date'] + "you wrote:"
		prefix = os.linesep + os.linesep + "On " + email_dict['Date'] + " <" + email_dict['Reply-To'] + "> wrote:" + os.linesep
		text = email_dict['Body']
		return prefix + "".join(["> " + x + os.linesep for x in text.splitlines()])
	else:
		return None

def composeGreeting(email_dict):
	if email_dict['First_name']:
		greeting = random.choice(['Dear', 'Hi', 'Hello'])
		return greeting + ' ' + email_dict['First_name'] + ',' + os.linesep
	else:
		return "Hello," + os.linesep

def composeSignoff(identity_dict):
	signoff = random.choice(['Kind Regards', 'Best Regards', 'Best Wishes', 'Warm Regards', 'Regards', 'Thanks', 'Thank you'])
	return signoff + ',' + os.linesep + random.choice([identity_dict['First_name'], " ".join([identity_dict['First_name'], identity_dict['Last_name']])])

def composeBody(text, email_class, identity_dict, email_dict, state):
#	body = getScenario(email_class + '/' + state + '/')
	## Figure out what other magic is necessary here. not sure how though?
	body = ""
	return body

def composeMessage(text, email_class, identity_dict, email_dict, state):
	message = ""
	message += composeGreeting(email_dict)
	if state==1:
		message += composeBody(text, email_class, identity_dict, email_dict, state)
	if hasPQ(text).values[0]:
		message += answerPQ(text, identity_dict, email_class)
	message += composeSignoff(email_dict)
	message += quoteText(email_dict)
	return message

def getFullEmail():
	return
