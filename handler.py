import pyinotify
import users_manager as u_manager
import core
import goodlog_manager as g_manager
import faillog_manager
import analyze as an
import Models
import log
import config

class EventHandler(pyinotify.ProcessEvent):
    def process_IN_MODIFY(self, event):
    	if event.pathname == '/var/log/wtmp':
    		core.Log_goodlog()

    	if event.pathname == '/var/log/auth.log':
    		core.Control_auth_log()

        log.Print("System zaznamenal zmenu v subore {0}", event.pathname)

def Start_capture():
	wm = pyinotify.WatchManager() # Watch Manager
	mask = pyinotify.IN_MODIFY # watched events
	u_manager.Get_dic_of_user()

	handler = EventHandler()
	notifier = pyinotify.Notifier(wm, handler)
	wdd_1 = wm.add_watch('/var/log/wtmp', mask, rec=True)
	dd_2 = wm.add_watch('/var/log/auth.log', mask, rec=True)
	notifier.loop()
