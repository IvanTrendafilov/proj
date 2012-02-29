import os
import poplib
import time
from email import parser
import random
def retrieveMessages(identity_dict):
	output_dir = 'incoming'
	pop_conn = poplib.POP3_SSL(identity_dict['Pop3'])
	pop_conn.user(identity_dict['Username'])
	pop_conn.pass_(identity_dict['Password'])
	messages = [pop_conn.retr(i) for i in range(1, len(pop_conn.list()[1]) + 1)]
	[pop_conn.dele(i) for i in range(1, len(pop_conn.list()[1]) + 1)]
	pop_conn.quit()
	messages = ["\n".join(mssg[1]) for mssg in messages]
	messages = [parser.Parser().parsestr(mssg) for mssg in messages]
	for msg in messages:
		replyto_addr = None
		output = ""
		unique_id = str(random.choice(xrange(1,999999999)))
		if msg['Reply-To']:
			replyto_addr = msg['Reply-To']
		else:
			replyto_addr = msg['From']
		output += "From: " + replyto_addr + os.linesep
		output += "To: " + msg['To'] + os.linesep
		output += "Date: " +  msg['Date'] + os.linesep
		output += "Subject: " + msg['Subject'] + os.linesep
		output += os.linesep
		output += msg.get_payload()
		tmpName = output_dir + '/' + 'IDENTITY' + '-' + unique_id + '.tmp', output_dir + '/' + 'IDENTITY' + '-' + unique_id + '.ready'
		tmpName, realName = 'IDENTITY' + '-' + unique_id + '.tmp', 'IDENTITY' + '-' + unique_id + '.ready' 
		f = open(tmpName, 'w')
		f.write(output)
		f.flush()
		os.fsync(f)
		f.close()
		os.rename(tmpName, realName)
	return

if __name__ == "__main__":
	while True:
		# Get the identity dict from a database somehow.
		retrieveMessages()
		time.sleep(60 * 5) #  5 mins