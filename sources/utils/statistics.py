#------------------------------------------------
from datetime import timedelta
from typing import List
from entities.Event import Event
#------------------------------------------------
class Statistics:

    def remove_unamed_activity(events : list) -> list[Event]:
        filtered = []

        for event in events:
            try:
                if event.name != None:
                    filtered.append(event)
            except:
                continue

        return filtered

    def group_duplicate_events_in_dict(self, data : dict):
        filtered = {}

        for category, ev_list in data.items():
            ev, _ = self.group_duplicate_events_in_list(ev_list)
            filtered.update({category: ev})

        return filtered

    def group_duplicate_events_in_list(events : list) -> tuple[List[Event], timedelta]:
        scoreboard_events = []
        total_time_amount = timedelta(0)

        for event in events:
            try:
                if event.name.upper() not in [e.name.upper() for e in scoreboard_events]:
                    scoreboard_events.append(event)
                    total_time_amount += event.duration
                else:
                    for ev in scoreboard_events:
                        if ev.name == event.name:
                            ev.duration += event.duration
                            total_time_amount += event.duration
                            break
            except:
                continue

        # Sort the events by total duration
        sorted_events = sorted(scoreboard_events, key=lambda x: x.duration, reverse=True)
        return sorted_events, total_time_amount

    def group_events_by_category(events : list, events_conf) -> dict:
        grouped_events = {}

        for section in events_conf.sections():
            grouped_events.update({section : []})
        grouped_events.update({events_conf.get('DEFAULT', 'DEFAULT_CATEGORY') : []})

        for section in events_conf.sections():
            try:
                row_words = events_conf.get(section, 'ALL_THAT_COUNTAINS')
            
                keywords = [word.strip().upper() for word in row_words.split(', ')]

                for index, event in enumerate(events):
                    if event.name is not None and any(keyword in event.name.upper() for keyword in keywords):
                        grouped_events[section].append(events.pop(index))
                    # else:
                    #     grouped_events[events_conf.get('DEFAULT', 'DEFAULT_CATEGORY')].append(events.pop(index))
            except:
                print("No ALL_THAT_COUNTAINS key in section", section)

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

        return duration_hours_by_category


