import random
def getRandomIdentity():
	identities = createIdentities()
	key = random.choice(list(identities.keys()))
	return (key, identities[key])

def createIdentities():
	identities = {}
	identities[0] = {'Gender': 'male', 'Age': '47', 'Marriage': 'Single', 'First_name': 'Ethan', 'Last_name': 'Stokes', 'Occupation': 'an accountant', 'Address': '21 Quay Street', 'City':'Manchester', 'Country':'UK','Postcode': 'M3 4AE', 'Telephone':'07425902430', 'Email': 'ethanstokes51@yahoo.co.uk', 'POP3': 'pop.mail.yahoo.com', 'SMTP': 'smtp.mail.yahoo.com', 'Username': 'ethanstokes51@yahoo.co.uk', 'Password': 'ethan2312'}
	identities[1] = {'Gender': 'male', 'Age': '35', 'Marriage': 'Single', 'First_name': 'Patrick', 'Last_name': 'Turner', 'Occupation': 'a sales assistant', 'Address': '83 King Street', 'City': 'Manchester', 'Country':'UK','Postcode': 'M2 4AH', 'Telephone':'07154942360', 'Email': 'patrick.turner1@gmx.com', 'POP3': 'pop.gmx.com', 'SMTP': 'mail.gmx.com', 'Username': 'patrick.turner1@gmx.com', 'Password': 'patrick5985!'}
	return identities

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