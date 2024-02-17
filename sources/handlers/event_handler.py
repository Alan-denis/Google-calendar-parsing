#------------------------------------------------
from datetime import datetime
import pytz
#------------------------------------------------

#------------------------------------------------
from sources.utils.calendar import *
from sources.utils.gui import *
from sources.utils.statistics import *

from main import event_list
from main import events_conf
#------------------------------------------------

#------------------------------------------------
def start_date_on_leave(event, start_date, canvas):

    parsed_date = datetime.strptime(start_date, '%Y-%m-%d')
    date_obj = datetime.combine(parsed_date, datetime.min.time(), tzinfo=pytz.UTC)

    filtered = filter_by_date(event_list, start_date=date_obj)
    grouped = group_events_category(filtered, events_conf)
    duration_by_category = calcul_duration_by_category(grouped)

    update_pie_chart(canvas, duration_by_category)


def end_date_on_leave(event, end_date, canvas):
    
    parsed_date = datetime.strptime(end_date, '%Y-%m-%d')
    date_obj = datetime.combine(parsed_date, datetime.min.time(), tzinfo=pytz.UTC)

    filtered = filter_by_date(event_list, end_date=date_obj)
    grouped = group_events_category(filtered, events_conf)
    duration_by_category = calcul_duration_by_category(grouped)

    update_pie_chart(canvas, duration_by_category)

def activity_filter(event, activity):
    print("ACTIVITY :",activity)
#------------------------------------------------