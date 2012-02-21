## C&C: Anti-419
from responder import composeMessage
from clean_email import extractInfo, removeHeaders
from email_classifier import classify
from dbconn import dbconn

def theLoop():
	## Read the directory with messages
	## Check if they exist
	## If they don't exist, assign them an identity
	## Do information extraction
	## Do email classification
	## compose response
	## repy
	## update the dbconn