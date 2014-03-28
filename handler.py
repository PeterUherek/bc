import pyinotify
import users_manager as u_manager
import main
import goodlog_manager as g_manager
import faillog_manager
import Models

wm = pyinotify.WatchManager() # Watch Manager
mask = pyinotify.IN_MODIFY # watched events

class EventHandler(pyinotify.ProcessEvent):
    def process_IN_MODIFY(self, event):
    	if event.pathname == '/var/log/wtmp':
    		main.Log_goodlog()

    	if event.pathname == '/var/log/auth.log':
    		main.Control_auth_log()

        print "Modify:", event.pathname


u_manager.Get_dic_of_user()



#hour_list = g_manager.Get_hour_list("03")
#num = faillog_manager.Get_number_of_faillog_from_last_password_change("2014-03-21",2)
#log = main.Log_faillog()
#um.Prin_dic_of_user()
#id = um.Get_user("peter")
#print id.good_log
#good.Add_log(id)

handler = EventHandler()
notifier = pyinotify.Notifier(wm, handler)
wdd_1 = wm.add_watch('/var/log/wtmp', mask, rec=True)
dd_2 = wm.add_watch('/var/log/auth.log', mask, rec=True)
notifier.loop()
