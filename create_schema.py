import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
engine = create_engine('sqlite:///master.db', echo=True)
metadata = MetaData()
classes = Table('classes', metadata,
	Column('class_id', Integer, primary_key=True), # class ID
	Column('desc', String), # what this class means
)
identities = Table('identities', metadata,
	Column('identity_id', Integer, primary_key=True), # identity ID
	Column('gender', String), 
	Column('age', String),
	Column('marriage', String),
	Column('first_name', String),
	Column('last_name', String),
	Column('occupation', String),
	Column('address', String),
	Column('city', String),
	Column('country', String),
	Column('postcode', String),
	Column('telephone', String),
	Column('email', String),
)
statuses = Table('statuses', metadata,
	Column('status_id', Integer, primary_key=True),
	Column('desc', String),
)
origins = Table('origins', metadata,
	Column('origin_id', Integer, primary_key=True),
	Column('desc', String),
)
messages = Table('messages', metadata,
	Column('msg_id', Integer, primary_key=True), # message ID
	Column('timestamp', String), # when the MSG was received
	Column('reply_addr', String), # Reply-To Addr
	Column('rcpt_addr', String), # Recepient Addr
	Column('msg_body', String), # Message Body
	Column('subject', String), # Email subject (if any)
)
conversations = Table('conversations', metadata,
	Column('conv_id', Integer, primary_key=True),
	Column('msg_id', None, ForeignKey('messages.msg_id')),
	Column('class_id', None, ForeignKey('classes.class_id')), # Spam Class ID
	Column('identity_id', None, ForeignKey('identities.identity_id')), # Which identity am I using? # think
	Column('status_id', None, ForeignKey('statuses.status_id')), # State from state table
	Column('origin_id', None, ForeignKey('origins.origin_id')), # where did I get it from?
)
metadata.create_all(engine) 
