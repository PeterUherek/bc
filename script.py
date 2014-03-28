import database_manager as d_manager
import Models as m
from random import randint



def Add_login(time_1,time_2):
	new_log = m.Good_log(user_id=2,ip_address="192.168.3.15",log_time=time_1,logoff_time = time_2)
	d_manager.Add_object(new_log)


def Add_logoff(line):
	session = d_manager.Get_session()
	timestamp = Get_timestamp(line,0)
	session.query(m.Good_log).filter_by(log_time=timestamp).update({"logoff_time": timestamp_2, "interval": line[14]})
	session.commit()


def Add(x,hour):

	i=0
	while x > i:
		day = randint(1,31)
		ran_1 = randint(0,59)
		ran_2 = randint(ran_1,59) 
		time_1 = "2014-03-%d %s:%d:00"%(day,hour,ran_1)
		time_2 = "2014-03-%d %s:%d:00"%(day,hour,ran_2)
		Add_login(time_1,time_2)
		i+=1
Add(64,"00")
Add(58,"01")
Add(45,"02")
Add(26,"03")
Add(5,"04")
Add(5,"05")
Add(2,"06")
Add(6,"07")
Add(8,"08")
Add(29,"09")
Add(144,"10")
Add(98,"11")
Add(92,"12")
Add(157,"13")
Add(227,"14")
Add(197,"15")
Add(168,"16")
Add(117,"17")
Add(89,"18")
Add(53,"19")
Add(59,"20")
Add(68,"21")
Add(87,"22")
Add(94,"23")