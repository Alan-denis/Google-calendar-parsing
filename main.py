#------------------------------------------------
from datetime import datetime
import pytz
import os
#------------------------------------------------

#------------------------------------------------
from sources.utils.calendar import *
from sources.utils.config import *
from sources.utils.carnivore import *
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

events_conf     = next((config for config in configurations if config.get('DEFAULT', 'NAME').upper() == "EVENTS"), None)
paths_conf      = next((config for config in configurations if config.get('DEFAULT', 'NAME').upper() == "PATHS"), None)
tasks_conf      = next((config for config in configurations if config.get('DEFAULT', 'NAME').upper() == "TASKS"), None)
gui_conf        = next((config for config in configurations if config.get('DEFAULT', 'NAME').upper() == "GUI"), None)
carnivore_conf  = next((config for config in configurations if config.get('DEFAULT', 'NAME').upper() == "CARNIVORE"), None)

config_obj = Config()
#------------------------------------------------

#------------------------------------------------
config_obj.calendar_ics_file_path = os.path.join(absolute_path, paths_conf.get('PATHS', 'CALENDAR'))
calendar = Calendar.read_calendar(config_obj.calendar_ics_file_path)

config_obj.event_list = Calendar.parse_events(calendar)


config_obj.carnivore_file_path = os.path.join(absolute_path, paths_conf.get('PATHS', 'CARNIVORE'))
entries = Carnivore.parse_input(config_obj.carnivore_file_path)

config_obj.carnivore_payment_history = entries

#------------------------------------------------

if __name__ == '__main__':
    start_gui()