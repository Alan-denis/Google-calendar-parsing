#------------------------------------------------
import icalendar
from datetime import datetime, date
import pytz
#------------------------------------------------

#------------------------------------------------
from entities.Event import Event
#------------------------------------------------
class Calendar:
    def read_calendar(ics_file):
        try:
            with open(ics_file, 'rb') as f:
                ics_file = icalendar.Calendar.from_ical(f.read())
        except:
            print("No calendar in configuration")
            
        return ics_file

    def parse_events(calendar):
        event_list = []

        for component in calendar.walk():

            if component.name == "VEVENT":
                event = Event()

                event.name = component.get('summary')
                event.start_date = component.get('dtstart').dt

                if type(event.start_date) == date:
                    event.start_date = datetime.combine(event.start_date, datetime.min.time(), pytz.UTC)

                try:
                    event.end_date = component.get('dtend').dt

                    if type(event.end_date) == date:
                        event.end_date = datetime.combine(event.end_date, datetime.min.time(), pytz.UTC)
                except:
                    event.end_date = event.start_date

                event.duration = event.end_date - event.start_date
                event.location = component.get('location')

                event_list.append(event)

        return event_list

    def filter_by_date(events, start_date : datetime = None, end_date : datetime = None) -> list[Event]:
        filtered_events = []

        for event in events:
            
            if start_date != None:
                if event.start_date < start_date:
                    # if the event's start_date is lesser than the start_date param, do not save the event
                    continue
            
            if end_date != None:
                if event.end_date > end_date:
                    # if the event's end_date is lesser than the end_date param, do not save the event
                    continue

            filtered_events.append(event)

        return filtered_events

    def filter_by_activity():
        pass