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
		print "\nExiting " + self.name

def analyze(threadName,log):
	vector = []
	user = u_manager.Get_user_2(log.user_id)
	if Exist_analyze(user) == True and user.lock == False:
		time_analyze(log,vector)
		vector.append(ip_analyze(log))
		vector.append(fail_count_analyze(log))
		vector.append(password_analyze(user))
		vector.append(Status_analyze(log,user))

		Print_vector(vector)
		Result(vector)

	else:
		print "Vsetky metriky sa nemohli vypocitat! Pretoze pouzivatel ma zablokovane heslo alebo je vymazany z databazy pouzivatelov."

def Result(vector):
	result = 0
	for v in vector:
		result += v
	result = (result/(vector.__len__()-1))
	print "\nVysledna metrika:", result

def Print_vector(vector):
	print "\n-----------------Faillog Analyza-------------------"
	print "Metrika zavisla od hodiny prihlasenia a ip adresy:", vector[0]
	print "Metrika zavisla od hodiny prihlasenia:", vector[1]
	print "Metrika zavisla od dna prihlasenia a ip adresy:", vector[2]
	print "Metrika zavisla od dna prihlasenia:", vector[3]
 	print "Metrika zavisla od ip adresy:", vector[4]
 	print "Metrika zavisla od poctu nespravnych prihlaseni:", vector[5]
 	print "Metirka zavisla od poslednej zmeny hesla:",vector[6]
 	print "Metrika zavisla od aktivity pouzivatela:",vector[7]

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

	def Get_score(profile_list,index):
		value = profile_list[index]
		#hour_list.sort(reverse=True)
		prefix = Get_prefix(profile_list)
		maximum_1 = Get_local_max(index,profile_list,Control_index_down,prefix)
		print "Maximum_1 je:", maximum_1
		maximum_2 = Get_local_max(index,profile_list,Control_index_up,prefix)
		print "Maximum_2 je:", maximum_2
		
		maximum = Get_max(maximum_1,maximum_2)

		if maximum == 0:
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
	print "Pocet good prihlaseni od poslednej zmeny hesla ", num_g
	print "Pocet fail prihlaseni od poslednej zmeny hesla ", num_f
	num = (num_g /(num_f+num_g))*100 
	print "Vysledne cislo je ",num
	return Get_fail_score(num)

def Status_analyze(log,user):
	log_1 = g_manager.Get_last_active_log(user.id) 
	log_2 = g_manager.Get_last_active_log_on_ip(user.id,log.ip_address)
	if log_1 is not None and log_2 is None:
		return 50
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






