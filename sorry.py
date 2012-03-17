import random
from smtplib import SMTP_SSL
from email.MIMEText import MIMEText
from responder import composeSignoff
from identity import getIdentityEmails, getIdentityByID
from main import init
import time
def sendRequest(conv_store):
	for key in conv_store:
		identity_dict = getIdentityByID(conv_store[key]['Identity_ID'])
		message = random.choice(['I am so sorry, but I accidentally deleted all my emails. Could you please resend your message?', 'I am terribly sorry, but I accidentally deleted your email before I had the chance to read it. Please resend it?', 'I am feeling stupid today. I deleted your message accidentally. Can you send it again to me, as it was?', 'Sorry! I carelessly deleted your earlier message. Can you resend it to me please?'])
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
		mime_msg['Subject'] = random.choice(['Apologies!',' ','Sorry....',' '])
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
