import os
import random
import string
from email_classifier import hasPQ
from string import Template
# identity_dict = {'Gender': 'male', 'Age': '47', 'Marriage': 'Single', 'First_name': 'Peter', 'Last_name': 'Donegan', 'Occupation':'an accountant', 'Address':'34 Cockburn Street', 'City':'Edinburgh', 'Country':'the UK', 'Postcode':'EH89LL', 'Telephone':'0742323123', 'Email':'peterdonegan64@yahoo.com'}

def preload():
	return {'Gender': 'male', 'Age': '47', 'Marriage': 'Single', 'First_name': 'Peter', 'Last_name': 'Donegan', 'Occupation':'an accountant', 'Address':'34 Cockburn Street', 'City':'Edinburgh', 'Country':'the UK', 'Postcode':'EH89LL', 'Telephone':'0742323123', 'Email':'peterdonegan64@yahoo.com'}

def countScenarios(scenario_name):
	return len(filter(lambda x: '.txt' in x and '~' not in x, os.listdir('scenarios/' + scenario_name + '/')))

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
	if state == 0:
		opening = os.linesep + getScenario(email_class + '/' + 'init') + os.linesep
		question_intro = os.linesep + getScenario(email_class + '/' + 'question_intro') + os.linesep
		question_count = random.choice(xrange(1, countScenarios(email_class + '/' + 'question_body'))) # Ask the person a random number of questions
		current_count, question_body = 0, ''
		while True:
			random_scenario = getScenario(email_class)
			if random_scenario not in question_body:
				question_body += random_scenario
				current_count += 1
			if current_count == question_count:
				break
		question_body = os.linesep + getScenario(email_class + '/' + 'question_body') + os.linesep
		body = "".join(opening, question_intro, question_body)
	else:
		body = "".join( [random.choice(string.letters[:26]) for i in xrange(300)] )  # this shall be removed
		# include here clever rules to determine what is going on
		# or consider building a learning agent
	return body

def composeMessage(text, email_class, identity_dict, email_dict, state):
	message = ""
	message += composeGreeting(email_dict)
	message += composeBody(text, email_class, identity_dict, email_dict, state)
	if hasPQ(text).values()[0]:
		message += answerPQ(text, identity_dict, email_class)
	message += composeSignoff(email_dict)
	message += quoteText(email_dict)
	return message

def getFullEmail():
	return
