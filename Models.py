from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy import ForeignKey
import database_manager as d_manager
from sqlalchemy.orm import relationship, backref



class User(d_manager.Base):
	__tablename__ = 'user'
	id = Column(Integer, primary_key=True)
	name = Column(String)
	fail_counter = Column(Integer)
	lock = Column(Boolean)
	change_time = Column(String)
	delete_time = Column(String)
	creation_time = Column(String)
	good_log = relationship("Good_log",order_by="Good_log.id",backref="user")
	fail_log = relationship("Fail_log",order_by="Fail_log.id",backref="user")
	def __repr__(self):
		return "<User(name='%s')>" % (self.name)


class Good_log(d_manager.Base):
	__tablename__ = 'good_log'
	id = Column(Integer, primary_key=True)
	ip_address = Column(String)
	console = Column(String)
	log_time = Column(String)
	logoff_time = Column(String)
	interval = Column(String)
	user_id = Column(Integer, ForeignKey('user.id'))
	#user = relationship("User",backref=backref('User.good_log',order_by=good_log_id))
	def __repr__(self):
		return "<Good_log(=id: '%s')>" % (self.id)


class  Fail_log(d_manager.Base):
	__tablename__='fail_log'
	id = Column(Integer, primary_key=True)
	ip_address = Column(String)
	time = Column(String)
	user_id = Column(Integer, ForeignKey('user.id'))
	def __repr__(self):
		return "<Fail_log(= id: '%s')>" % (self.id)