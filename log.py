import config
import logging 

print_on_terminal = True
logger = logging.getLogger('IDSystem')
def Get_print_on_terminal():
	value = config.Record_terminal()
	print_on_terminal=value

def Get_logger():
	logger.setLevel(logging.INFO)

	# create console handler and set level to debug
	link = config.Get_log_file()
	ch = logging.FileHandler(link)
	ch.setLevel(logging.INFO)
	# create formatter
	format = config.Log_format()
	formatter = logging.Formatter(format)

	# add formatter to ch
	ch.setFormatter(formatter)

	# add ch to logger
	logger.addHandler(ch)


def Log_block_ip(log):
	if(config.Log_ip_address()==True):
		text="Blokovanie ip adresy: {0}"
		logger.info(text.format(log.ip_address))
		Print(text,log.ip_address)

def Log_block_user(user):
	if(config.Log_user()==True):
		text="Blokovanie uzivatela: {0}"
		logger.info(text.format(user))
		Print(text,user)

def Log_hazard(hazard,user,ip_address):
	if(config.Record_hazard()==True):
		if(user=="invalid"):
			user = "UNKNOW"
		text = 'Miera ohrozenia: {0} Uzivatel: {1} IP_adresa: {2}'
		logger.info('Miera ohrozenia: %d Uzivatel: %s IP_adresa: %s'%(hazard,user,ip_address))
		Print(text,hazard,user,ip_address)

def Print(arg,*form):
	if(print_on_terminal==True):
		if(form==None):
			print(arg)
		else:
			print(arg.format(*form))

