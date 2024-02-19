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
def filter_date_on_leave(event, start_date, end_date, canvas, bar_charts_list):

    try:
        parsed_date = datetime.strptime(start_date, '%Y-%m-%d')
        date_obj_start = datetime.combine(parsed_date, datetime.min.time(), tzinfo=pytz.UTC)
    except:
        date_obj_start = None

    try:
        parsed_date = datetime.strptime(end_date, '%Y-%m-%d')
        date_obj_end = datetime.combine(parsed_date, datetime.max.time(), tzinfo=pytz.UTC)
    except:
        date_obj_end = None
        
    filtered = filter_by_date(event_list, date_obj_start, date_obj_end)

    grouped = group_events_by_category(filtered, events_conf)
    print(grouped)
    duration_by_category = calcul_duration_by_category(grouped)

    update_pie_chart(canvas, duration_by_category)
    update_bar_charts(bar_charts_list, grouped)

def activity_filter(event, activity):
    print("ACTIVITY :",activity)

def update_bar_charts(bar_chart_ax_list : list, data : dict):
    x_label = "label"
    y_label = "Value"

    for category, events in data.items():
        print("Category:", category)

        ax_chart = None
        for ax in bar_chart_ax_list:
            if category == ax.get_title():
                ax_chart = ax
                break

        if ax_chart is not None:
            event_data = []

            for event in events:
                # Create a DataFrame for each event
                event_data.append({x_label: event.name, y_label: event.duration.total_seconds() / 3600})
                # event_data.append({x_label: event.name, y_label: 4})
            
            print(event_data)

            # Concatenate event DataFrames with the existing chart_data
            event_df = pd.DataFrame(event_data)

            # Plot the updated chart
            event_df.plot(kind='bar', x=x_label, y=y_label, ax=ax_chart)

    # Refresh the canvas to reflect the changes
    for ax in bar_chart_ax_list:
        ax.figure.canvas.draw()

def update_pie_chart(canvas, data : dict):
    # do not show the TOTAL_TIME to the pie chart 
    reference_amount = data.pop('TOTAL_TIME')

    fig, ax = plt.subplots()
    ax.pie(data.values(), labels=data.keys(), autopct='%1.1f%%')
    ax.set_title(gui_conf.get('PIE_CHART_BY_CATEGORY', 'NAME'))

    canvas.figure = fig
    canvas.draw()

def on_configure(event, canvas):
    canvas.configure(scrollregion=canvas.bbox('all'))
#------------------------------------------------