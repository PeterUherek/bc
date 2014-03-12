from __future__ import division
import threading
import Models as m
import faillog_manager as f_manager
import goodlog_manager as g_manager

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
	hour_analyze()
	ip_analyze()
	fail_count_analyze()


def hour_analyze():
	hour_list = g_manager.Get_hour_list("03")
	index = int("03")
	value = hour_list[index]
	hour_list.sort(reverse=True)
	maximum = hour_list[0]
	print maximum
	print value
	f_score = (value / maximum)*100
	print f_score

def ip_analyze():
	f_num = f_manager.Get_number_user_faillog_on_sepecific_ip(log)
	g_num = g_manager.Get_number_user_goodlog_on_specific_ip(log)
	num = ((f_num+g_num)/f_num)*100
	print "Pocet tejto ip: "+log.ip_address+ " f_num: %d a g_num: %d numje: %f %%" %(f_num,g_num,num)

def fail_count_analyze():
