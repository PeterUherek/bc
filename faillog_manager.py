import database_manager as d_manager
import users_manager as u_manager
from time import gmtime, strftime
import Models as m

def Control_and_push_faillog(line):
	session = d_manager.Get_session()
	user_id = u_manager.Get_user_id(line[8])
	timestamp = Get_Timestamp(line)
	count=0
	if user_id == 0:
		count=2
	log = session.query(m.Fail_log).filter_by(user_id=user_id,time=timestamp).first()
	print log
	if log is None:
		return Add_faillog(line,timestamp,user_id,count)
	else:
		return None
	
def Add_faillog(line,timestamp,user_id,count):
	print "Pridal som objekt"
	new_log = m.Fail_log(user_id=user_id,time=timestamp,ip_address=line[10+count])
	d_manager.Add_object(new_log)
	return new_log

def Get_Timestamp(line):
	year = strftime(" %Y",gmtime())
	tim = line[0]+" "+line[1]+" "+line[2]+year
	return strftime(tim)

def Get_number_user_faillog_on_sepecific_ip(log):
	session = d_manager.Get_session()
	num = session.query(m.Fail_log).filter_by(ip_address=log.ip_address, user_id=log.user_id).count()
	return num
