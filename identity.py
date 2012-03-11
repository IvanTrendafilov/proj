import random
def getRandomIdentity():
	identities = createIdentities()
	key = random.choice(list(identities.keys()))
	return (key, identities[key])

def getIdentityEmails():
	identities = createIdentities()
	return [identities[identity]['Email'] for identity in identities]

def getIdentityByName(first_name, last_name):
	if first_name and last_name:
		allIDs = createIdentities()
		for identity in allIDs:
			if (allIDs[identity]['First_name'].lower() == first_name.lower()) and (allIDs[identity]['Last_name'].lower() == last_name.lower()):
				return (identity, allIDs[identity])
	return None

def getIdentityByEmail(email_addr):
	allIDs = createIdentities()
	for identity in allIDs:
		if allIDs[identity]['Email'] == email_addr:
			return (identity, allIDs[identity])
 	return None
 
def getIdentityByID(ID):
	allIDs = createIdentities()
	try:
		return allIDs[ID]
	except KeyError:
		return None

def createIdentities():
	identities = {}
	identities[0] = {'Gender': 'male', 'Age': '47', 'Marriage': 'Single', 'First_name': 'Ethan', 'Last_name': 'Stokes', 'Occupation': 'an accountant', 'Address': '21 Quay Street', 'City':'Manchester', 'Country':'UK','Postcode': 'M3 4AE', 'Telephone':'07425902430', 'Email': 'ethanstokes51@yahoo.co.uk', 'POP3': 'pop.mail.yahoo.com', 'SMTP': 'smtp.mail.yahoo.com', 'Username': 'ethanstokes51@yahoo.co.uk', 'Password': 'ethan2312'}
	identities[1] = {'Gender': 'male', 'Age': '35', 'Marriage': 'Single', 'First_name': 'Patrick', 'Last_name': 'Turner', 'Occupation': 'a sales assistant', 'Address': '83 King Street', 'City': 'Manchester', 'Country':'United Kingdom','Postcode': 'M2 4AH', 'Telephone':'07154942360', 'Email': 'patrick.turner1@gmx.com', 'POP3': 'pop.gmx.com', 'SMTP': 'mail.gmx.com', 'Username': 'patrick.turner1@gmx.com', 'Password': 'patrick5985!'}
	identities[2] = {'Gender': 'male', 'Age': '39', 'Marriage': 'Single', 'First_name': 'Leo', 'Last_name': 'Brookes', 'Occupation': 'a store owner', 'Address': '11 Lordswood Road', 'City': 'Birmingham', 'Country':'England','Postcode': 'B17 9RP', 'Telephone':'07851832724', 'Email': 'leo.brooks11@yahoo.com', 'POP3': 'pop.mail.yahoo.com', 'SMTP': 'smtp.mail.yahoo.com', 'Username': 'leo.brooks11@yahoo.com', 'Password': 'leo12321d9'}
	identities[3] = {'Gender': 'male', 'Age': '51', 'Marriage': 'Single', 'First_name': 'Zachary', 'Last_name': 'Bray', 'Occupation': 'a welder', 'Address': '20 Claredale Street', 'City': 'London', 'Country': 'England','Postcode': 'E2 6PF', 'Telephone':'07427342732', 'Email': 'zachary.bray@gmx.com', 'POP3': 'pop.gmx.com', 'SMTP': 'mail.gmx.com', 'Username': 'zachary.bray@gmx.com', 'Password': 'zack12y37'}
	identities[4] = {'Gender': 'male', 'Age': '45', 'Marriage': 'Single', 'First_name': 'Daniel', 'Last_name': 'Palmer', 'Occupation': 'an accountant ', 'Address': 'Coley Hill', 'City': 'Reading', 'Country':'England','Postcode': 'RG1 6AE', 'Telephone':'07622352282', 'Email': 'daniel.palmer61@gmx.com', 'POP3': 'pop.gmx.com', 'SMTP': 'mail.gmx.com', 'Username': 'daniel.palmer61@gmx.com', 'Password': 'daniel36128as'}
	return identities