import os
import random
import string
import time
from email_classifier import hasPQ
from string import Template
from smtplib import SMTP_SSL
from smtplib import SMTP
from email.MIMEText import MIMEText

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
	intro = getScenario('pq_intro') + os.linesep
	ending = os.linesep + getScenario('pq_ending') + os.linesep
	marriage = ""
	if email_class == 'romance':
		marriage = getScenario('marriage')
	if "....." in text or "_____" in text:
		body = getScenario('pq_generic')
		paragraph = os.linesep + ''.join([intro + os.linesep, body, os.linesep + ending]) + os.linesep
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

def composeSubject(email_dict):
	return "Re: " + email_dict['Subject']

def composeMessage(text, email_class, identity_dict, email_dict, state):
	message = (2 * os.linesep).join(['$Greeting', '$Body', '$Signoff', '$QuotedText'])
	message = message.replace(os. linesep + '$QuotedText', '$QuotedText')
	content = {'Greeting': composeGreeting(email_dict), 'Body': composeBody(text, email_class, identity_dict, email_dict, state), 'Signoff': composeSignoff(identity_dict), 'QuotedText': quoteText(email_dict)}
	return Template(message).safe_substitute(content)


def buildQuestionBody(email_class, maxscen = 4):
	question_count = random.choice(range(2, min(maxscen, countScenarios(email_class + '/' + 'question_body'))))
	current_count, question_body = 0, ''
	while True:
		random_scenario = getScenario(email_class + '/' + 'question_body')
		if random_scenario not in question_body:
			question_body += random_scenario + os.linesep
			current_count += 1
		if current_count == question_count:
			break
	return question_body

def composeBody(text, email_class, identity_dict, email_dict, state):
	content, body = {}, (2 * os.linesep).join(['$Opening', '$PQ_answer', '$Question_intro', '$Question_body'])
	if state == 0 and hasPQ(text).values()[0]:
		content['Opening'] = getScenario(email_class + '/' + 'init')
		content['PQ_answer'] = answerPQ(text, identity_dict, email_class)
		content['Question_intro'] = getScenario(email_class + '/' + 'question_intro')
		content['Question_body'] = buildQuestionBody(email_class)
	elif state == 0:
		body.replace('$PQ_answer' + os.linesep * 2, '')
		content['Opening'] = getScenario(email_class + '/' + 'init')
		content['Question_intro'] = getScenario(email_class + '/' + 'question_intro')
		content['Question_body'] = buildQuestionBody(email_class)
	else:
		body = "".join([random.choice(string.letters[:26]) for i in xrange(300)])  # nothing meaningful yet
	return Template(body).safe_substitute(content)

def composeSignoff(identity_dict):
	signoff = random.choice(['Kind Regards', 'Best Regards', 'Best Wishes', 'Warm Regards', 'Regards', 'Thanks', 'Thank you'])
	return signoff + ',' + os.linesep + random.choice([identity_dict['First_name'], " ".join([identity_dict['First_name'], identity_dict['Last_name']])])

def sendEmail(text, email_class, identity_dict, email_dict, state):
	try:
		message = composeMessage(text, email_class, identity_dict, email_dict, state)
		own_addr = identity_dict['Email']
		destination_addr = email_dict['Reply-To']
		text_subtype = 'plain'
		mime_msg = MIMEText(message, text_subtype)
		mime_msg['Subject'] = composeSubject(email_dict)
		mime_msg['From'] = own_addr
		mime_msg['To'] = destination_addr
		if 'yahoo' in own_addr:
			server_addr = identity_dict['SMTP']
#			server_addr = 'smtp.mail.yahoo.com'
			conn = SMTP_SSL(server_addr)
			conn.set_debuglevel(False)
			conn.login(identity_dict['Username'], identity_dict['Password'])
			try:
				conn.sendmail(own_addr, destination_addr, mime_msg.as_string())
			finally:
				print "Send email!"
				conn.close()
	except Exception:
		return None
	return {'Date': time.ctime(), 'Reply-To': own_addr, 'To': destination_addr, 'Subject': composeSubject(email_dict), 'Body': message, 'Attachment': 0, 'First_name': identity_dict['First_name'], 'Last_name': identity_dict['Last_name']}