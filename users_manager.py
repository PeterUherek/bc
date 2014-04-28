import database_manager as d_manager
import Models as m
import log

dic_of_user = {}

def Control_user(user,timestamp):
	if dic_of_user.__contains__(user)==False:
		Add_user(user,timestamp)
		log.Print("System zaznamenal pridanie noveho pouzivatela menom {0}",user)


def Add_user(key,timestamp):
	"""
	Toto je upravne a netestovane
	"""
	#session = d_manager.Get_session()
	new_user = m.User(name=key,lock=False,fail_counter=0,creation_time=timestamp,change_time=timestamp)
	d_manager.Add_object(new_user)
	#session.add(new_user)
	#session.commit()
	Update_dic_of_user(key)

def Get_user_id(key):
	return dic_of_user[key]
	
def Get_user(key):
	session = d_manager.Get_session()
	user = session.query(m.User).filter_by(name=key).one()
	session.close()
	return user

def Get_user_2(key):
	session = d_manager.Get_session()
	user = session.query(m.User).filter_by(id=key).one()
	session.close()
	return user

def Update_dic_of_user(key):
	session = d_manager.Get_session()
	user = session.query(m.User).filter_by(name=key).one()
	dic_of_user[key] = user.id
	session.close()

def Get_dic_of_user():
	session = d_manager.Get_session()
	for user in session.query(m.User).all():
		dic_of_user[user.name]=user.id
	Print_dic_of_user()
	session.close()
	


def Print_dic_of_user():
	print "--------------Vypis vsetkych pouzivatelov------------------"
	count = 0
	for user in dic_of_user:
		count+=1
		print"No.",count ," Meno:",user, " ID:", dic_of_user[user]
	pass

def Update_user(key,column,value):
	session = d_manager.Get_session()
	session.query(m.User).filter_by(name=key).update({column : value})
	session.commit()
	session.close()

def Update_fail_counter(key,value):
	Update_user(key,"fail_counter",value)

def Add_one_to_fail_counter(key):
	user = Get_user(key)
	value = user.fail_counter + 1
	Update_fail_counter(key,value)

def Lock_user(key,value):
	Update_user(key,"lock",value)
	if(value==True):
		log.Print("System zaznamenal blokovanie pouzivatela menom {0}",key)
	else:
		log.Print("System zaznamenal odblokovznie pouzivatela menom {0}",key)

def Password_changed_time(key,value):
	Update_user(key,"change_time",value)
	log.Print("System zaznamenal zmenu hesla pouzivatela menom {0}",key)

def Remove_user(key,value):
	Update_user(key,"delete_time",value)
	log.Print("System zaznamenal vymazanie pouzivatela menom {0}",key)