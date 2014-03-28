import database_manager as d_manager
import users_manager as u_manager
from time import gmtime, strftime
import Models as m


def Add_log(line):
	if line[8] != '-':
		Add_login(line)
	else:
		Add_logoff(line)

def Add_login(line):
	user = u_manager.Get_user(line[0])
	timestamp = Get_timestamp(line,0)
	new_log = m.Good_log(user_id=user.id,console=line[1],ip_address=line[2],log_time= timestamp)
	d_manager.Add_object(new_log)
	u_manager.Update_fail_counter(user.name,0)

def Add_logoff(line):
	session = d_manager.Get_session()
	timestamp = Get_timestamp(line,0)
	timestamp_2 =Get_timestamp(line,6)
	session.query(m.Good_log).filter_by(log_time=timestamp).update({"logoff_time": timestamp_2, "interval": line[14]})
	session.commit()


def Get_timestamp(line,count):	
	c=3+count
	tim = (line[c]+" "+line[c+1]+" "+line[c+2]+" "+line[c+3]+" "+line[c+4])
	timestamp = strftime(tim)
	return timestamp

def Get_number_user_goodlog_on_specific_ip(log):
	session = d_manager.Get_session()
	num = session.query(m.Good_log).filter_by(user_id=log.user_id,ip_address=log.ip_address).count()
	return num

def Get_number_login_per_month(month):
	session = d_manager.Get_session()
	q = d_manager.Get_extract('month',m.Good_log.log_time)
	return session.query(m.Good_log).filter(q == month).count()

def Get_number_login_per_hour_and_month(month,hour):
	session = d_manager.Get_session()
	q = d_manager.Get_extract('month',m.Good_log.log_time)
	p = d_manager.Get_extract('hour',m.Good_log.log_time)
	return session.query(m.Good_log).filter(q == month,p == hour).count()
	


def Get_hour_list(month,key,flag,ip):
	session = d_manager.Get_session()
	q = d_manager.Get_extract('month',m.Good_log.log_time)
	p = d_manager.Get_extract('hour',m.Good_log.log_time)
	hour = 0
	hour_list = []
	while hour < 24:
		if flag is "IP":
			count = session.query(m.Good_log).filter(q == month,p == hour).filter_by(user_id=key,ip_address=ip).count()
		else:
			count = session.query(m.Good_log).filter(q == month,p == hour).filter_by(user_id=key).count()
		hour_list.append(count)
		hour += 1
	return hour_list

def Get_day_list(month,key,flag,ip):
	session = d_manager.Get_session()
	q = d_manager.Get_extract('month',m.Good_log.log_time)
	d = d_manager.Get_extract('dow',m.Good_log.log_time)
	day = 0
	day_list = []
	while day < 7:
		if flag is "IP":
			count = session.query(m.Good_log).filter(q == month,d == day).filter_by(user_id=key,ip_address=ip).count()
		else:
			count = session.query(m.Good_log).filter(q == month,d == day).filter_by(user_id=key).count()
		day_list.append(count)
		day += 1
	return day_list

def Get_number_of_goodlog_from_last_password_change(timestamp,key):
	session = d_manager.Get_session()
	q = d_manager.Get_and(m.Good_log.user_id,key,m.Good_log.log_time,timestamp)
	num = session.query(m.Good_log).filter(q).count()
	return num

def Get_last_active_log(key):
	session = d_manager.Get_session()
	log = session.query(m.Good_log).filter_by(user_id=key,logoff_time=None).first()
	return log

def Get_last_active_log_on_ip(key,ip):
	session = d_manager.Get_session()
	log = session.query(m.Good_log).filter_by(user_id=key,logoff_time=None,ip_address=ip).first()
	return log