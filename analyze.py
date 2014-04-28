from __future__ import division
from config import Metrics
import threading
import Models as m
import users_manager as u_manager
import faillog_manager as f_manager
import goodlog_manager as g_manager
import datetime
import log 

class Thread (threading.Thread):
	def __init__(self, threadID, name, log):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.log = log
		self.hazard = 0
	def run(self):
		log.Print("Analyza neuspesneho prihlasenia pre prihlasenie cislo {0} sa zacala",self.log.id)
		result = analyze(self.name, self.log)
		self.hazard = result
		

def analyze(threadName,log):

	vector = []
	weight = Metrics()
	user = u_manager.Get_user_2(log.user_id)
	if(user.name!="invalid"):
		vector.append(Exist_analyze(user,weight))
		time_analyze(log,vector,user,weight)
		vector.append(ip_analyze(log,user,weight))

		vector.append(fail_count_analyze(log,weight))
		vector.append(Interval_analyze(user,weight))
		vector.append(password_analyze(user,weight))
		vector.append(Status_analyze(log,user,weight))
	else:
		weight_2 = []
		weight_2.append(weight[0])
		weight_2.append(weight[5])
		weight_2.append(weight[7])
		weight = weight_2
		vector.append(Exist_analyze(user,weight))
		vector.append(ip_analyze(log,user,weight))
		vector.append(Interval_analyze(user,weight))

	Print_vector(vector,user,weight)
	return Result(vector,weight)
	
		
def Result(vector,weight):
	result = 0
	w = 0
	for i in range(0,vector.__len__()):
		result += vector[i]*weight[i]
		w += weight[i]
		#print "Vaha", weight[i]
		#print "Hodnota", vector[i]
	result = (result/w)
	log.Print("\nVysledna metrika: {0}", result)
	return result

def Print_vector(vector,user,weight):
	def Algin_printer(text,v,w):
		for i in range(text.__len__()-1,53):
			text += " "
		text += " %d"%(v)
		for i in range(text.__len__()-1,58):
			text += " "
		text += "Vaha metriky: %1.2f"%(w)
		log.Print(text)

	print vector.__len__()
	print weight.__len__()

	print "\n-------------------------Faillog Analyza--------------------------------------"
	if(user.name != "invalid"):
		print "Pouzivatel: %s"%user.name
		Algin_printer("Metrika zavisla od moznosti pristupu pouzivatela k OS:",vector[0],weight[0])
		Algin_printer("Metrika zavisla od hodiny prihlasenia a ip adresy:",vector[1],weight[1])
		Algin_printer("Metrika zavisla od hodiny prihlasenia:",vector[2],weight[2])
		Algin_printer("Metrika zavisla od dna prihlasenia a ip adresy:",vector[3],weight[3])
		Algin_printer("Metrika zavisla od dna prihlasenia:",vector[4],weight[4])
	 	Algin_printer("Metrika zavisla od ip adresy:",vector[5],weight[5])
	 	Algin_printer("Metrika zavisla od poctu neuspesnych prihlaseni:",vector[6],weight[6])
	 	Algin_printer("Metrika zavisla od intezity neuspesnych prihlaseni:",vector[7],weight[7])
	 	Algin_printer("Metirka zavisla od poslednej zmeny hesla:",vector[8],weight[8])
	 	Algin_printer("Metrika zavisla od aktivity pouzivatela:",vector[9],weight[9])
	else:
	 	print "Pouzivatel: UNKNOW"
	 	Algin_printer("Metrika zavisla od moznosti pristupu pouzivatela k OS:",vector[0],weight[0])
	 	Algin_printer("Metrika zavisla od ip adresy:",vector[1],weight[1])
	 	Algin_printer("Metrika zavisla od intezity neuspesnych prihlaseni:",vector[2],weight[2])
 	

def Exist_analyze(user,weight):
	if user.name == "invalid":
		return 100
	if user.delete_time == None and user.lock == False:
		weight.pop(0)
		weight.insert(0,0)
		return 0
	if user.delete_time == None and user.lock == True:
		#weight.append(1)
		return 0
	if user.delete_time != None:
		#weight.append(1)
		ttm_1 = user.delete_time
		ttm_2 = datetime.datetime.now()
		ttm = ttm_2 - ttm_1
		x = ttm.days / 30
		x = int(x)
		if x > 10:
			x = 10
		return x*10


def Get_month(timestamp,user):
	def Get_time(c_timestamp):
		c_month = c_timestamp.strftime('%m')
		c_year = c_timestamp.strftime('%Y')
		c_month = int(c_month)
		c_year = int(c_year)
		return c_month,c_year

	def Compare(c_month,m_month,user,c_year,m_year):
		c_num = g_manager.Get_number_login_per_month_for_concrete_user(user.id,c_month,c_year)
		m_num = g_manager.Get_number_login_per_month_for_concrete_user(user.id,m_month,m_year)
		#print "NUm", c_num,m_num
		if c_num > m_num and c_num > 20:
			return c_month
		elif m_num > c_num and m_num > 20:
			return m_month
		else:
			return None

	#c_month,c_year = Get_time(user.creation_time)
	m_month,m_year = Get_time(timestamp)
	if(m_month == 1):
		return Compare(12,m_month,user,m_year,m_year-1)
	else:
		#print "Tunak 4",c_month,m_year
		return Compare(m_month-1,m_month,user,m_year,m_year-1)

	"""
	if(m_month == c_month and c_year == m_year):
		print "Tunak 1",c_month,m_year
		return m_month
	if(m_month == c_month+1 and m_year == c_year):
		print "Tunak 2 ",c_month,m_year
		return Compare(c_month,m_month,user)
	if(c_month == 12 and m_year == c_year+1):
		print "Tunak 3",c_month,m_year	
		return Compare(c_month,m_month,user)	 

	if(m_month == 1):
		return 12
	else:
		print "Tunak 4",c_month,m_year
		return m_month-1
	"""

def time_analyze(log,vector,user,weight):
	
	def Control_index_down(index,x):
		if index != 0:
			return (index-1)
		else:
			return x
	def Control_index_up(index,x):
		if index != x:
			return (index+1)
		else:
			return 0
			
	def Get_local_max(index,profile_list,foo,prefix):
		origin = profile_list[index]
		index = foo(index,prefix)
		current = profile_list[index]
		while origin < current:
			index = foo(index,prefix)
			origin = current
			current = profile_list[index]
		return origin

	def Get_prefix(profile_list):
		if profile_list.__len__() == 24:
 			return 23
		else:
			return 6

	def Get_max(maximum_1,maximum_2):
		if maximum_2 > maximum_1:
			return maximum_2
		else: 
			return maximum_1

	def Get_score(profile_list,index,weight,w):
		value = profile_list[index]
		#hour_list.sort(reverse=True)
		prefix = Get_prefix(profile_list)
		maximum_1 = Get_local_max(index,profile_list,Control_index_down,prefix)
		maximum_2 = Get_local_max(index,profile_list,Control_index_up,prefix)
		
		maximum = Get_max(maximum_1,maximum_2)

		if maximum == 0:
			#print "Metrika zavisla od casu nema vypovednu hodnotu!"
			weight.pop(w)
			weight.insert(w,0)
			return 0
		f_score = (value / maximum)*100
		f_score = 100-f_score
		#print "Maximum je: %d Value je %d  a Hour_failscore je: %f"%(maximum,value,f_score)
		#weight.append(1)
		return Get_fail_score(f_score)

	t = log.time
	print t
	tim = datetime.datetime.strptime(t,"%b %d %H:%M:%S %Y")
	month = Get_month(tim,user)
	#print "Mesiac",month
	if(month == None):
		for i in range(1,5):
			vector.append(0)
			weight.pop(i)
			weight.insert(i,0)
		return

	hour = tim.strftime('%H')
	day = tim.strftime('%w')
	index_hour = int(hour)
	index_day = int(day)

	time_list = g_manager.Get_hour_list(month,log.user_id,"IP",log.ip_address)
	vector.append(Get_score(time_list,index_hour,weight,1))

	time_list = g_manager.Get_hour_list(month,log.user_id,"N",log.ip_address)
	vector.append(Get_score(time_list,index_hour,weight,2))

	time_list = g_manager.Get_day_list(month,log.user_id,"IP",log.ip_address)
	vector.append(Get_score(time_list,index_day,weight,3))

	time_list = g_manager.Get_day_list(month,log.user_id,"N",log.ip_address)
	vector.append(Get_score(time_list,index_day,weight,4))
	pass

def ip_analyze(log,user,weight):
	if(user.name!="invalid"):
		f_num = f_manager.Get_number_user_faillog_on_specific_ip(log)
		g_num = g_manager.Get_number_user_goodlog_on_specific_ip(log)
	else:
		f_num = f_manager.Get_number_faillog_on_specific_ip(log)
		g_num = g_manager.Get_number_goodlog_on_specific_ip(log)

	num = ((f_num)/(f_num+g_num))*100
	#print "Pocet tejto ip: "+log.ip_address+ " f_num: %d a g_num: %d numje: %f %%" %(f_num,g_num,num)
	return Get_fail_score(num)

def fail_count_analyze(log,weight):
	user = u_manager.Get_user_2(log.user_id)
	#print "User menom %s a jeho fail counter %d" %(user.name,user.fail_counter)
	return Get_fail_score(user.fail_counter*10)

def Interval_analyze(user,weight):
	failog_list = f_manager.Get_last_ten_faillog(user.id)
	counter = 0
	last = 0
	interval = []
	for log in failog_list:
		#print log
		counter += 1
		if last == 0:
			last = log.time
			continue
		new = log.time
		interval.append(last-new)
		last = new

	if counter <= 1:
		weight.pop(7)
		weight.insert(7,0)
		print counter
		return 0
			
	result = 0
	for i in range(1,interval.__len__()):
		print interval[i]
		if(interval[0]+datetime.timedelta(seconds=10) >= interval[i] and interval[0]-datetime.timedelta(seconds=10)<= interval[i]):
			result += 1
		else:
 			return result*10
 	return result*10



def password_analyze(user,weight):
	if user.change_time == None:
		#print "Metrika zavisla od zmeny hesla nema vypovednu hodnotu!"
		weight.pop(8)
		weight.insert(8,0)
		return 0
	num_f = f_manager.Get_number_of_faillog_from_last_password_change(user.change_time,user.id)
	num_g = g_manager.Get_number_of_goodlog_from_last_password_change(user.change_time,user.id)
	#print "User si menil heslo ", user.change_time
	#print "Pocet good prihlaseni od poslednej zmeny hesla ", num_g
	#print "Pocet fail prihlaseni od poslednej zmeny hesla ", num_f
	num = (num_g /(num_f+num_g))*100 
	#print "Vysledne cislo je ",num
	return Get_fail_score(num)

def Status_analyze(log,user,weight):
	log_1 = g_manager.Get_last_active_log(user.id) 
	log_2 = g_manager.Get_last_active_log_on_ip(user.id,log.ip_address)
	if log_1 is not None and log_2 is None:
		return 100
	else:
		weight.pop(9)
		weight.insert(9,0) 
		return 0

def Get_fail_score(num):
	i=0
	result = 0
	while i != 100:
		if num > i:
			result += 1
		i += 1
 	return result

