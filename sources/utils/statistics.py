#------------------------------------------------
from datetime import datetime, timedelta
from typing import List
from entities.Event import Event
#------------------------------------------------

def order_events_by_duration(events) -> tuple[List[Event], timedelta]:
    scoreboard_events = []
    total_time_amount = timedelta(0)

    for event in events:
        if event.name not in [e.name for e in scoreboard_events]:
            scoreboard_events.append(event)
            total_time_amount += event.duration
        else:
            for ev in scoreboard_events:
                if ev.name == event.name:
                    ev.duration += event.duration
                    total_time_amount += event.duration
                    break

    # Sort the events by total duration
    sorted_events = sorted(scoreboard_events, key=lambda x: x.duration, reverse=True)
    return sorted_events, total_time_amount

def group_events_category(events, events_conf) -> dict:
    grouped_events = {}

    for section in events_conf.sections():
        grouped_events.update({section : []})
    grouped_events.update({'OTHER' : []})

    for section in events_conf.sections():
        row_words = events_conf.get(section, 'ALL_THAT_COUNTAINS')
        keywords = [word.strip().upper() for word in row_words.split(', ')]

        for event in events:
            if any(keyword in event.name.upper() for keyword in keywords):
                grouped_events[section].append(event)

    return grouped_events

def calcul_duration_by_category(events_by_category) -> dict:
    duration_by_category = {}

    for key in events_by_category.keys():
        duration_by_category.update({key: timedelta(0)})
    duration_by_category.update({'TOTAL_TIME': timedelta(0)})

    for category in events_by_category.keys():
        for event in events_by_category[category]:
            duration_by_category[category] += event.duration
            duration_by_category['TOTAL_TIME'] += event.duration

    # Convert timedelta values to number of hours (float)
    duration_hours_by_category = {}
    for key, value in duration_by_category.items():
        duration_hours_by_category[key] = value.total_seconds() / 3600.0

    print(duration_hours_by_category)

    return duration_hours_by_category