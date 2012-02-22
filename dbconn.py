from singleton import Singleton
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey, Sequence
import os


class dbconn(object):
	__metaclass__ = Singleton
	engine, metadata, classes, identities, statuses, origins, messages, conversations = 0, 0, 0, 0, 0, 0, 0, 0

	def __init__(self, db_location='sqlite://///' + os.environ['HOME'] + '/dev/proj/data/main.memory'):
		self.engine = create_engine(db_location, echo=True)
		self.create_schema(self.engine)
		return

	def create_schema(self, engine):
		self.metadata = MetaData()
		self.classes = Table('classes', self.metadata,
			Column('class_id', Integer, primary_key=True),  # class ID
			Column('desc', String),  # what this class means
		)
		self.identities = Table('identities', self.metadata,
			Column('identity_id', Integer, primary_key=True),  # identity ID
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
			Column('username', String),
			Column('password', String),
			Column('pop3', String),
			Column('smtp', String),
		)
		self.statuses = Table('statuses', self.metadata,
			Column('status_id', Integer, primary_key=True),
			Column('desc', String),
		)
		self.origins = Table('origins', self.metadata,
			Column('origin_id', Integer, primary_key=True),
			Column('desc', String),
		)
		self.attachments = Table('attachments', self.metadata,
			Column('msg_id', Integer),
			Column('filename', String),
			Column('extension', String),
		)
		self.messages = Table('messages', self.metadata,
			Column('msg_id', Integer, primary_key=True),  # message ID
			Column('date', String),  # when the MSG was received
			Column('reply_addr', String),  # Reply-To Addr
			Column('rcpt_addr', String),  # Recepient Addr
			Column('subject', String),  # Email subject (if any)
			Column('msg_body', String),  # Message Body
			Column('attachment', Integer), # This is really a Boolean
			Column('reply_first_name', String),
			Column('reply_last_name', String),
		)
		self.conversations = Table('conversations', self.metadata,
			Column('conv_id', Integer, Sequence('user_id_seq'), primary_key=True),
			Column('msg_id', None, ForeignKey('messages.msg_id')),
			Column('class_id', None, ForeignKey('classes.class_id')),  # Spam Class ID
			Column('identity_id', None, ForeignKey('identities.identity_id')),  # Which identity am I using? # think
			Column('status_id', None, ForeignKey('statuses.status_id')),  # State from state table
			Column('origin_id', None, ForeignKey('origins.origin_id')),  # where did I get it from?
		)
		self.hashes = Table('hashes', self.metadata,
			Column('hash', String), 
		)
		self.metadata.create_all(engine)
		return
