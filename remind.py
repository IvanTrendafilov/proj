import random
from smtplib import SMTP_SSL
from email.MIMEText import MIMEText
from responder import composeSignoff
from identity import getIdentityEmails, getIdentityByID
from main import init
import time
def sendRequest(conv_store):
	for key in conv_store:
		if conv_store[key]['State'] == 'CLOSED' or key < 36:
			continue;
		identity_dict = getIdentityByID(conv_store[key]['Identity_ID'])
		message = random.choice(['Hello', 'Hi'])
		message += '\n'
		message += random.choice(['I have not heard from you in a while. I was wondering if everything is OK? Shall we proceed?', 
			'I am concerned about you. Is everything alright? I have not heard from you in a while and am beginning to worry. Please reply back to let me know if we shall proceed? Please let me know about the next steps.', 
			'I have not heard anything from you for a couple of days now. I am beginning to worry. Is everything OK? Shall we go on? If so, please let me know about the next steps. Thank you!'
			])
		message += '\n'
		message += composeSignoff(identity_dict)
		own_addr = identity_dict['Email']
		own_name = ' '.join([identity_dict['First_name'], identity_dict['Last_name']])
		bucket = conv_store[key]['Bucket']
		mime_msg = MIMEText(message, 'plain')
		mime_msg['From'] = own_name + ' <' + own_addr + '>'
		if not bucket:
			continue
		else:
			destination_addr = bucket[0]
		for email_addr in bucket:
			if email_addr not in getIdentityEmails():
				mime_msg['To'] = email_addr
		if conv_store[key]['Messages'][0]['Subject']:
			mime_msg['Subject'] = "Re: " + conv_store[key]['Messages'][0]['Subject']
		else:
			mime_msg['Subject'] = "Re: "
		server_addr = identity_dict['SMTP']
		conn = SMTP_SSL(server_addr)
		conn.set_debuglevel(True)
		conn.login(identity_dict['Username'], identity_dict['Password'])
		try:
			print "Preview:\n"
			print mime_msg.as_string()
			conn.sendmail(own_addr, destination_addr, mime_msg.as_string())
		finally:
			print "Send email!"
			conn.close()
			time.sleep(5)	

if __name__ == "__main__":
	a, b = init()
	del b[0]
	sendRequest(b)
