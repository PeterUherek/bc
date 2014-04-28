import ConfigParser
import ast 

def Get_Parser():
	config = ConfigParser.RawConfigParser()
	config.read('config.txt')
	return config

def ConfigSectionMap(section):
    dict1 = {}
    Config = Get_Parser()
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1

def Database_Connection():
	connect = ConfigSectionMap("Databaza")['connection_string']
	return connect 

def Metrics():
	metrics = ConfigSectionMap("Metriky")
	weight = []
	for m in metrics:
		w = int(metrics[m])
		weight.append(w)
	return weight

def Block_ip_address():
	Config = Get_Parser()
	block_ip = Config.getboolean("Blokovanie", "ip_adresy")
	return block_ip

def Block_ip_address_value():
	value = ConfigSectionMap("Blokovanie")['ip_adresy_od_ohorzenia']
	return float(value) 

def Log_ip_address():
	Config = Get_Parser()
	return Config.getboolean("Logovanie", "log_block_ip")

def Get_log_file():
	value = ConfigSectionMap("Logovanie")['info_log_file_path']
	return value

def Log_user():
	Config = Get_Parser()
	return Config.getboolean("Logovanie", "log_bloc_user")

def Block_user():
	Config = Get_Parser()
	block_user = Config.getboolean("Blokovanie", "uzivatelia")
	return block_user

def Block_user_value():
	value = ConfigSectionMap("Blokovanie")['uzivatelia_od_ohrozenia']
	return float(value) 

def Record_hazard():
	Config = Get_Parser()
	return Config.getboolean("Logovanie", "log_threat")

def Record_hazard_value():
	value = ConfigSectionMap("Logovanie")['log_threat_from']
	return float(value) 

def Record_terminal():
	Config = Get_Parser()
	return Config.getboolean("Logovanie", "print_on_terminal")

def Log_format():
	Config = Get_Parser()
	value = Config.get("Logovanie","log_format")
	return value

def Unblock_ip_addres():
	Config = Get_Parser()
	value = Config.get("Blokovanie","zakazane_blokovanie_ip_adries")
	value = value.replace(" ", "")
	value = value.split(",")
	dic = {}
	for i in value:
		dic[i] = None
	return dic
