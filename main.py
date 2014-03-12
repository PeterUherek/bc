import os
import users_manager as u_manager
import goodlog_manager as g_manager
import faillog_manager as f_manager
import analyze

def Log_goodlog():
	line = Execute_command("last -iwF")
	u_manager.Control_user(line[0])
	g_manager.Add_log(line)

def Log_faillog():
	process = os.popen("tail /var/log/auth.log | grep \"Failed\"")
	lines = process.readlines()
	process.close()
	print lines
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

