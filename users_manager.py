import database_manager as d_manager
import Models as m


dic_of_user = {}

def Control_user(user):
	if dic_of_user.__contains__(user):
		print "obsahuje"
	else:
		print "neobsahuje"
		Add_user(user)

def Add_user(key):
	session = d_manager.Get_session()
	new_user = m.User(name=key)
	session.add(new_user)
	session.commit()
	Update_dic_of_user(key)
	Update_fail_counter(key,0)

def Get_user_id(key):
	return dic_of_user[key]
	
def Get_user(key):
	session = d_manager.Get_session()
	user = session.query(m.User).filter_by(name=key).one()
	return user

def Get_user_2(key):
	session = d_manager.Get_session()
	user = session.query(m.User).filter_by(id=key).one()
	return user

def Update_dic_of_user(key):
	session = d_manager.Get_session()
	user = session.query(m.User).filter_by(name=key).one()
	dic_of_user[key] = user.id

def Get_dic_of_user():
	session = d_manager.Get_session()
	for user in session.query(m.User).all():
		print "User traala :", user.name, ":", user.id
		dic_of_user[user.name]=user.id
	pass;


def Print_dic_of_user():
	print "Vypis vsetkych userov"
	count = 0
	for user in dic_of_user:
		count+=1
		print"User cislo:",count ," Meno:",user, " ID: ", dic_of_user[user]
	pass

def Update_fail_counter(key,value):
	session = d_manager.Get_session()
	session.query(m.User).filter_by(name=key).update({"fail_counter": value})
	session.commit()

def Add_one_to_fail_counter(key):
	user = Get_user(key)
	value = user.fail_counter + 1
	Update_fail_counter(key,value)

