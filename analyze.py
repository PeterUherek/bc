from __future__ import division
import threading
import Models as m
import users_manager as u_manager
import faillog_manager as f_manager
import goodlog_manager as g_manager
import datetime

class Thread (threading.Thread):
	def __init__(self, threadID, name, log):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.log = log
	def run(self):
		print "Starting " + self.name
		analyze(self.name, self.log)
		print "Exiting " + self.name

def analyze(threadName,log):
	vector = []
	user = u_manager.Get_user_2(log.user_id)
	if Exist_analyze(user) == True and user.lock == False:
		time_analyze(log,vector)
		vector.append(ip_analyze(log))
		vector.append(fail_count_analyze(log))
		vector.append(password_analyze(user))

	print vector

def Exist_analyze(user):
	if user.delete_time is None:
		return True
	else: 
		print "Uzivatel nefiguruje v zozname!"
		return False

	"""
	Spravim priemer 
	"""
	"""
	timestamp = log.time
	print timestamp
	month = timestamp.strftime('%m')
	hour = timestamp.strftime('%H')
	overall = g_manager.Get_number_login_per_month(month)
	value = g_manager.Get_number_login_per_hour_and_month(month,hour)
	f_score = (value / overall) * 100
	print "Overall je: %d Value je %d  a Hour_failscore je: %f"%(overall,value,f_score)
	"""

def time_analyze(log,vector):
	def Get_score(hour_list,index):
		value = hour_list[index]
		hour_list.sort(reverse=True)
		maximum = hour_list[0]
		print maximum
		print value
		if maximum is 0:
			print "Metrika nema vypovednu hodnotu!"
			return 0
		f_score = (value / maximum)*100
		f_score = 100-f_score
		print "Maximum je: %d Value je %d  a Hour_failscore je: %f"%(maximum,value,f_score)
		return Get_fail_score(f_score)

	timestamp = log.time
	hour = timestamp.strftime('%H')
	month = timestamp.strftime('%m')
	day = timestamp.strftime('%w')
	index_hour = int(hour)
	index_day = int(day)

	time_list = g_manager.Get_hour_list(month,log.user_id,"IP",log.ip_address)
	vector.append(Get_score(time_list,index_hour))

	time_list = g_manager.Get_hour_list(month,log.user_id,"N",log.ip_address)
	vector.append(Get_score(time_list,index_hour))

	time_list = g_manager.Get_day_list(month,log.user_id,"IP",log.ip_address)
	vector.append(Get_score(time_list,index_day))

	time_list = g_manager.Get_day_list(month,log.user_id,"N",log.ip_address)
	vector.append(Get_score(time_list,index_day))
	pass

def ip_analyze(log):
	f_num = f_manager.Get_number_user_faillog_on_sepecific_ip(log)
	g_num = g_manager.Get_number_user_goodlog_on_specific_ip(log)
	num = ((f_num)/(f_num+g_num))*100
	print "Pocet tejto ip: "+log.ip_address+ " f_num: %d a g_num: %d numje: %f %%" %(f_num,g_num,num)
	return Get_fail_score(num)

def fail_count_analyze(log):
	user = u_manager.Get_user_2(log.user_id)
	print "User menom %s a jeho fail counter %d" %(user.name,user.fail_counter)
	return Get_fail_score(user.fail_counter*10)

def password_analyze(user):
	num_f = f_manager.Get_number_of_faillog_from_last_password_change(user.change_time,user.id)
	num_g = g_manager.Get_number_of_goodlog_from_last_password_change(user.change_time,user.id)
	print "User si menil heslo ", user.change_time
	print "Pocet good prihlaseni od poslednej zmeni hesla ", num_g
	print "Pocet fail prihlaseni od poslednej zmeni hesla ", num_f
	num = (num_g /(num_f+num_g))*100 
	print "Vysledne cislo je ",num
	return Get_fail_score(num)

def Status_analyze(log,user):
	log_1 = g_manager.Get_last_active_log(user.id) 
	log_2 = g_manager.Get_last_active_log_on_ip(user.ip,log.ip_address)
	if log_1 is not None and log_2 is None:
		return 100
	else: 
		return 0

def Get_fail_score(num):
	i=0
	result = 0
	while i != 100:
		if num > i:
			result += 1
		i += 1
 	return result






