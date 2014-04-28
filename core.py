from os import popen
import users_manager as u_manager
import goodlog_manager as g_manager
import faillog_manager as f_manager
from analyze import Thread
import config
import log as logger

def Log_goodlog():
	line = Execute_command("last -iwF")
	g_manager.Add_log(line)

def Control_auth_log():
	New_user()
	Delete_User()
	Log_faillog()
	Block()
	Changed_password()

	
def Block():
	lines = Get_lines_from_auth_log("changed by")
	for line in lines:
		line = line.split()
		name = line[7]
		line = Execute_command("passwd -S "+name)
		name = name.strip("'")
		if line[1] == 'L':
			u_manager.Lock_user(name,True)
		else:
			u_manager.Lock_user(name,False)

def Changed_password():
	lines = Get_lines_from_auth_log("password changed")
	for line in lines:
		line = line.split()
		name = line[9]
		line = Execute_command("passwd -S "+name)
		u_manager.Password_changed_time(name,line[2])
		
def Get_lines_from_auth_log(key):
	process = popen("tail /var/log/auth.log | grep \""+key+"\"")
	lines = process.readlines()
	process.close()
	return lines

def New_user():
	lines = Get_lines_from_auth_log("new user")
	for line in lines:
		line = line.split()
		timestamp = f_manager.Get_Timestamp(line)
		line = line[7].split("=")
		line = line[1].strip(",")
		u_manager.Control_user(line,timestamp)

def Delete_User():
	lines = Get_lines_from_auth_log("delete user")
	for line in lines:
		line = line.split()
		user = line[7].strip("'")
		timestamp = f_manager.Get_Timestamp(line)
		u_manager.Remove_user(user,timestamp)

def Log_faillog():
	lines = Get_lines_from_auth_log("Failed")
	for line in lines:
		line = line.split()
		log = f_manager.Control_and_push_faillog(line)
		if log != None:
			Start_analyze(log)


def Execute_command(command):
	l = popen(command)
	line = l.readline()
	line = line.split()
	return line

def Start_analyze(log):
	try:
		thread = Thread(1,"Thread-1",log)
		thread.start()
		thread.join()
		Analyze_result(thread)
	except:
		print "Error: Analyze hasn't started"


def Analyze_result(thread):
	user = u_manager.Get_user_2(thread.log.user_id)
	if(config.Record_hazard_value()<=float(thread.hazard)):
		logger.Log_hazard(thread.hazard,user.name,thread.log.ip_address)

	if(config.Block_ip_address()==True):
		if(config.Block_ip_address_value()<=float(thread.hazard)):
			if(config.Unblock_ip_addres().__contains__(thread.log.ip_address)==False):
				Blocking_ip_address(thread.log)

	if(config.Block_user()==True and user.lock==False):
		if(config.Block_user_value()<=float(thread.hazard)):
			Blocking_user(thread.log,user)


def Blocking_user(log,user):
	command = "passwd -l %s"%user.name
	try:
		popen(command)
		logger.Log_block_user(user.name)
	except:
		print "Error: Blokovanie pouzivatela zlyhalo"

def Blocking_ip_address(log):
	command = "iptables -A INPUT -s %s -j DROP"%(log.ip_address)
	try:
		popen(command)
		f = open('/etc/hosts.deny','a')
		f.write('sshd: {0}\n'.format(log.ip_address))
		f.close()
		logger.Log_block_ip(log)
	except:
		print "Error: BLokovanie adresy zlyhalo"




command = logger.Block_ip_command()
popen(command)