#------------------------------------------------
from datetime import datetime
import pytz
import os
#------------------------------------------------

#------------------------------------------------
from sources.utils.calendar import *
from sources.utils.config import *
from sources.utils.statistics import *

from view.body import *
# from view.test import *
#------------------------------------------------

#------------------------------------------------
absolute_path = os.path.dirname(__file__)
#------------------------------------------------

#------------------------------------------------
conf_path = os.path.join(absolute_path, "configurations")
configurations = Config.read_configuration_files(conf_path)

events_conf = next((config for config in configurations if config.get('DEFAULT', 'NAME').upper() == "EVENTS"), None)
paths_conf  = next((config for config in configurations if config.get('DEFAULT', 'NAME').upper() == "PATHS"), None)
tasks_conf  = next((config for config in configurations if config.get('DEFAULT', 'NAME').upper() == "TASKS"), None)
gui_conf    = next((config for config in configurations if config.get('DEFAULT', 'NAME').upper() == "GUI"), None)

config_obj = Config()
#------------------------------------------------

#------------------------------------------------
ics_file_path = os.path.join(absolute_path, paths_conf.get('PATHS', 'CALENDAR'))
config_obj.calendar_ics_file_path = ics_file_path

calendar = Calendar.read_calendar(config_obj.calendar_ics_file_path)
event_list = Calendar.parse_events(calendar)
#------------------------------------------------

if __name__ == '__main__':
    start_gui()