from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import extract, and_, func


engine = create_engine('postgresql://postgres:asdf456@localhost:5432/Log', echo=False)
Base = declarative_base()
Base.metadata.create_all(engine)

def Get_session():
	Session = sessionmaker(bind=engine)
	return Session()

def Add_object(new_object):
	session = Get_session()
	session.add(new_object)
	session.commit()
	
def Get_extract(time,model_column):
	return extract(time,model_column)

def Get_and(model_column,user_id,model_column_2,value_2):
	return and_(model_column == user_id, model_column_2 > value_2)

def Get_Max(model_column):
	return func.Max(model_column)