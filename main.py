#------------------------------------------------
from datetime import datetime
import pytz
import os
#------------------------------------------------

#------------------------------------------------
from sources.utils.calendar import *
from sources.utils.config import *
from sources.utils.statistics import *
#------------------------------------------------

#------------------------------------------------
absolute_path = os.path.dirname(__file__)
#------------------------------------------------

#------------------------------------------------
conf_path = os.path.join(absolute_path, "configurations")
configurations = read_configuration_files(conf_path)

events_conf = next((config for config in configurations if config.get('DEFAULT', 'NAME').upper() == "EVENTS"), None)
paths_conf  = next((config for config in configurations if config.get('DEFAULT', 'NAME').upper() == "PATHS"), None)
tasks_conf  = next((config for config in configurations if config.get('DEFAULT', 'NAME').upper() == "TASKS"), None)
#------------------------------------------------

#------------------------------------------------
ics_file_path = os.path.join(absolute_path, paths_conf.get('PATHS', 'CALENDAR'))
#------------------------------------------------

if __name__ == '__main__':
    calendar = read_calendar(ics_file_path)
    event_list = parse_events(calendar)
    filtered = filter_by_date(event_list, datetime(2024, 2, 12, 6, 15, tzinfo=pytz.UTC))

    ladderboard, total_time_amount = order_events_by_duration(filtered)

    print(calcul_duration_by_category(group_events_categorie(filtered, events_conf)))

    # for event in ladderboard:
    #     print(event.name, ":", round(event.duration / total_time_amount * 100, 2))