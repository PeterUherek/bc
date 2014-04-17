import os
import users_manager as u_manager
import goodlog_manager as g_manager
import faillog_manager as f_manager
import analyze

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
		print line
		line = line.split()
		name = line[7]
		print "Idem niekoho blokovat ",name
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
		print "Meno", name
		line = Execute_command("passwd -S "+name)
		print "Cas", line[2]
		u_manager.Password_changed_time(name,line[2])
		
def Get_lines_from_auth_log(key):
	process = os.popen("tail /var/log/auth.log | grep \""+key+"\"")
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
		print line
		u_manager.Control_user(line,timestamp)

def Delete_User():
	lines = Get_lines_from_auth_log("delete user")
	for line in lines:
		line = line.split()
		user = line[7].strip("'")
		print "User",user
		timestamp = f_manager.Get_Timestamp(line)
		u_manager.Remove_user(user,timestamp)

def Log_faillog():
	lines = Get_lines_from_auth_log("Failed")
	for line in lines:
		line = line.split()
		#print "Toto je line", line
		log = f_manager.Control_and_push_faillog(line)
		if log is not None:
			Start_analyze(log)

	"""
	line =line.readlines()
	line = line[2].split()
	u_manager.Control_user(line[0])
	new_log = f_manager.Add_faillog(line)
	return new_log
	"""

def Execute_command(command):
	l = os.popen(command)
	line = l.readline()
	line = line.split()
	return line

def Start_analyze(log):
	try:
		thread = analyze.Thread(1,"Thread-1",log)
		thread.start()
	except:
		print "Error: Analyze hasn't started"





#new = ""
#print("NOVE:"+ file_line)
#print("Stare:"+exec_line)

#count=0
#while exec_line != file_line:
#	new = new + exec_line
#	exec_line = l.readline()
#	print(exec_line)
#	count= count +1

