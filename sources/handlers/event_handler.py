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
from main import gui_conf
#------------------------------------------------

#------------------------------------------------
def filter_date_on_leave(event, start_date, end_date, pie_chart_ax, bar_charts_list):

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

    no_duplicates = group_duplicate_events_in_dict(grouped)
    duration_by_category = calcul_duration_by_category(no_duplicates)

    update_pie_chart(pie_chart_ax, duration_by_category)
    update_bar_charts(bar_charts_list, no_duplicates)

def activity_filter(event, activity):
    print("ACTIVITY :",activity)

def update_bar_charts(bar_chart_ax_list : list, data : dict):
    x_label = "Label"
    y_label = "Value"

    for category, events in data.items():
        ax_chart = None
        for ax in bar_chart_ax_list:
            if category == ax.get_title():
                ax_chart = ax
                break

        if ax_chart is not None:
            title = ax_chart.get_title()
            ax_chart.cla()
            ax_chart.set_title(title)

            event_data = []
            for event in events:
                event_data.append({x_label: event.name, y_label: event.duration.total_seconds() / 3600})

            try:
                event_df = pd.DataFrame(event_data)
                event_df = event_df.sort_values(by=y_label, ascending=False)

                event_df.plot(kind='bar', x=x_label, y=y_label, ax=ax_chart, color=gui_conf.get('BAR_CHARTS', 'BARS_COLOR'))
            except:
                print("No data in the", title, "chart")

    # Refresh the canvas to reflect the changes
    for ax in bar_chart_ax_list:
        ax.grid(axis='y', linestyle=gui_conf.get('BAR_CHARTS', 'VERTICAL_LIGNES_STYLE'), 
                linewidth=gui_conf.get('BAR_CHARTS', 'VERTICAL_LIGNES_WIDTH'), 
                color=gui_conf.get('BAR_CHARTS', 'VERTICAL_LIGNES_COLOR'))
        ax.figure.canvas.draw()

def update_pie_chart(ax, data : dict):
    # do not show the TOTAL_TIME to the pie chart 
    reference_amount = data.pop('TOTAL_TIME')
    title = ax.get_title()
    ax.cla()

    ax.pie(data.values(), labels=data.keys(), autopct='%1.1f%%')
    ax.set_title(title)
    ax.figure.canvas.draw()

def on_configure(event, canvas):
    canvas.configure(scrollregion=canvas.bbox('all'))
#------------------------------------------------