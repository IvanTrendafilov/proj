import random
def getRandomIdentity():
	return random.choice(createIdentities())

def createIdentities():
	id1 = {'Gender': 'male', 'Age': '47', 'Marriage': 'Single', 'First_name': 'Ethan', 'Last_name': 'Stokes', 'Occupation': 'an accountant', 'Address': '21 Quay Street', 'City':'Manchester', 'Country':'UK','Postcode': 'M3 4AE', 'Telephone':'07425902430', 'Email': 'ethanstokes51@yahoo.co.uk', 'POP3': 'pop.mail.yahoo.com', 'SMTP': 'smtp.mail.yahoo.com', 'Username': 'ethanstokes51@yahoo.co.uk', 'Password': 'ethan2312'}
	return [id1]

def getIdentityByName(first_name, last_name):
	if first_name and last_name:
		allIDs = createIdentities()
		for identity in allIDs:
			if (identity['First_name'].lower() == first_name.lower()) and (identity['Last_name'].lower() == last_name.lower()):
				return identity
	return None

def getIdentityByEmail(email_addr):
	allIDs = createIdentities()
	for identity in allIDs:
		if identity['Email'] == email_addr:
			return identity
 	return None
