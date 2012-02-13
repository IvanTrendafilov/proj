import os
import random
from string import Template
# identity_dict = {'Gender': 'male', 'Age': '47', 'Marriage': 'Single', 'First_name': 'Peter', 'Last_name': 'Donegan', 'Occupation':'an accountant', 'Address':'34 Cockburn Street', 'City':'Edinburgh', 'Country':'the UK', 'Postcode':'EH89LL', 'Telephone':'0742323123', 'Email':'peterdonegan64@yahoo.com'}

def getScenario(curr_dir):
	options = filter(lambda x: '.txt' in x and '~' not in x, os.listdir(curr_dir))  #  love for FP
	return open(curr_dir + random.choice(options)).read().strip()

def answerPQ(text, identity_dict, text_class='romance'):
	paragraph = ""
	postcode_words = ['post code', 'postcode', 'zip']
	intro = getScenario('scenarios/pq_intro/')
	ending = getScenario('scenarios/pq_ending/')
	if text_class == 'romance':
		marriage = getScenario('scenarios/marriage/')
	if "....." in text or "_____" in text:
		body = getScenario('scenarios/pq_generic/')
		paragraph = os.linesep + " ".join([intro, body, ending])
	else:
		name = getScenario('scenarios/name/')
		occupation = getScenario('scenarios/occupation/')
		age = getScenario('scenarios/age/')
		location = getScenario('scenarios/location/')
		postcode = ""
		for word in postcode_words:
			if word in text.lower():
				postcode = getScenario('scenarios/postcode/')
				break
		contact = getScenario('scenarios/contact/')
		paragraph = os.linesep + " ".join([intro, name, occupation, age, marriage, location, postcode, contact, ending])
	paragraph = Template(paragraph).safe_substitute(identity_dict)
	return paragraph