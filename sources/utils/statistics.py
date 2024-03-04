#------------------------------------------------
from datetime import timedelta, datetime
from typing import List
#------------------------------------------------

#------------------------------------------------
from entities.Event import Event
#------------------------------------------------

class Statistics:
    class Calendar:
        def remove_unamed_activity(events : list) -> list[Event]:
            filtered = []

            for index, event in enumerate(events):
                if event.name != None:
                    filtered.append(event)
                else:
                    events.pop(index)
                    continue

            return filtered

        def group_duplicate_events_in_dict(self, data : dict):
            filtered = {}

            for category, ev_list in data.items():
                ev, _ = self.group_duplicate_events_in_list(ev_list)
                filtered.update({category: ev})

            return filtered

        def group_duplicate_events_in_list(events : list):
            scoreboard_events = []
            total_time_amount = timedelta(0)

            for index, event in enumerate(events):

                found = False
                for scoreboard_event in scoreboard_events:
                    if event.name.upper() == scoreboard_event.name.upper():
                        scoreboard_event.duration += event.duration
                        total_time_amount += event.duration
                        events.pop(index)
                        found = True
                        break

                if not found:
                    scoreboard_events.append(events.pop(index))
                    total_time_amount += event.duration

            sorted_events = sorted(scoreboard_events, key=lambda x: x.duration, reverse=True)
            return sorted_events, total_time_amount

        def group_events_by_category(events : list, events_conf) -> dict:
            grouped_events = {}

            for section in events_conf.sections():
                grouped_events.update({section : []})

            for section in events_conf.sections():
                try:
                    row_words = events_conf.get(section, 'ALL_THAT_COUNTAINS')
                
                    keywords = [word.strip().upper() for word in row_words.split(', ')]
                    
                    for index, event in enumerate(events):
                        if event.name is not None and any(keyword in event.name.upper() for keyword in keywords):
                            grouped_events[section].append(events.pop(index))

                except:
                    print("No ALL_THAT_COUNTAINS key in section", section)

            for index, event in enumerate(events):
                        grouped_events[events_conf.get('DEFAULT', 'DEFAULT_CATEGORY')].append(events.pop(index))

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

    class Carnivore:
        def calculate_total_cost_by_month(entries : list) -> dict:
            total_amount_by_mounth = {}

            for entry in entries:
                date_str, price = entry[0], entry[3]
                date = datetime.strptime(date_str, "%d/%m/%Y")
                month_year = date.strftime("%m/%Y")

                total_amount_by_mounth[month_year] = total_amount_by_mounth.get(month_year, 0.00) + price

            return total_amount_by_mounth
        
        def calculate_month_span(entries: list):
            month_spans = {}

            for entry in entries:
                date_str = entry[0]
                date = datetime.strptime(date_str, "%d/%m/%Y")
                month_year = date.strftime("%m/%Y")
                
                if month_year not in month_spans:
                    # Initialize with the current date for both min and max
                    month_spans[month_year] = {'min': date, 'max': date}
                else:
                    # Update min and max dates if necessary
                    month_spans[month_year]['min'] = min(month_spans[month_year]['min'], date)
                    month_spans[month_year]['max'] = max(month_spans[month_year]['max'], date)
                    
            span_by_month = {}
            for date, values in month_spans.items():
                span_by_month.update({date : values['max'] - values['min'] + timedelta(days=1)})

            return span_by_month
        
        def calculate_total_cost_by_type(entries : list):
            pass
        
        def calculate_average_spent_per_month(entries: list):
            span_by_month = Statistics.Carnivore.calculate_month_span(entries)
            total_cost_per_month = Statistics.Carnivore.calculate_total_cost_by_month(entries)

            average_spent_per_month = {}
            for month_year, total_spent in total_cost_per_month.items():
                count = span_by_month[month_year].days

                try:
                    average_spent_per_month[month_year] = total_spent / count
                except:
                    average_spent_per_month[month_year] = 0.00  # or any other default value

            return average_spent_per_month