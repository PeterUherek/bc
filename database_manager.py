from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import extract, and_, func, desc
import config
import log


connection_string = config.Database_Connection()
try:
	engine = create_engine(connection_string, echo=False)
	Base = declarative_base()
	Base.metadata.create_all(engine)
	log.Print("Vytvorenie spojenia do databazy sa podarilo!")	
except: 
	log.Print("Vytvorenie spojenia zlyhalo!")


def Get_session():
	Session = sessionmaker(bind=engine,expire_on_commit=False)
	return Session()

def Add_object(new_object):
	session = Get_session()
	session.add(new_object)
	session.commit()
	session.close()
	
def Get_extract(time,model_column):
	return extract(time,model_column)

def Get_and(model_column,user_id,model_column_2,value_2):
	return and_(model_column == user_id, model_column_2 > value_2)

def Get_Max(model_column):
	return func.Max(model_column)

def Get_desc(model_column):
	return desc(model_column)