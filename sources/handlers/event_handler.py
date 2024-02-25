#------------------------------------------------
from datetime import datetime, time
import pytz
import re
from tkinter import messagebox
#------------------------------------------------

#------------------------------------------------
from sources.utils.calendar import *
from sources.utils.gui import *
from sources.utils.statistics import *

from main import event_list as el
from main import events_conf as ec
from main import gui_conf as gc
#------------------------------------------------

#------------------------------------------------
def filter_date_on_leave(event, pie_chart, bar_chart_canvas, start_date: str, end_date : str, filter_start : bool, filter_end : bool):
    if filter_start:
        try:
            parsed_date = datetime.strptime(start_date, '%d-%m-%Y')
            date_obj_start = datetime.combine(parsed_date, datetime.min.time(), tzinfo=pytz.UTC)
        except:
            messagebox.showinfo("Date format no respected", "The date format desn't respect the 'dd-mm-yyyy' format, therefore no date is used as a reference.")
            date_obj_start = None
    else:
        date_obj_start = None

    if filter_end:
        try:
            parsed_date = datetime.strptime(end_date, '%d-%m-%Y')
            date_obj_end = datetime.combine(parsed_date, datetime.max.time(), tzinfo=pytz.UTC)
        except:
            messagebox.showinfo("Date format no respected", "The date format desn't respect the 'dd-mm-yyyy' format, therefore the today's end date is used as a reference.")
            current_time = datetime.max.time()
            date_obj_end = datetime.combine(date.today(), time(current_time.hour, current_time.minute, current_time.second), tzinfo=pytz.UTC)
    else:
        date_obj_end = None

    filtered = Calendar.filter_by_date(el, date_obj_start, date_obj_end)
    # filtered = remove_unamed_activity(filtered)

    no_duplicates, _ = Statistics.group_duplicate_events_in_list(filtered)
    grouped = Statistics.group_events_by_category(no_duplicates, ec)

    duration_by_category = Statistics.calcul_duration_by_category(grouped)

    update_pie_chart(pie_chart, duration_by_category)
    update_bar_charts(bar_chart_canvas, grouped)

def activity_filter(event, activity):
    print("ACTIVITY :",activity)

def update_bar_charts(bar_chart_canvas : FigureCanvasTkAgg, data : dict):
    x_label = "Label"
    y_label = "Value"

    axes_list = bar_chart_canvas.figure.axes

    for category, events in data.items():
        ax_chart = None
        for ax in axes_list:
            if category == ax.get_title():
                ax_chart = ax
                break

        if ax_chart is not None:
            title = ax_chart.get_title()
            ax_chart.clear()
            ax_chart.set_title(title)

            event_data = []
            for event in events:
                event_data.append({x_label: event.name, y_label: event.duration.total_seconds() / 3600})

            try:
                event_df = pd.DataFrame(event_data)
                event_df = event_df.sort_values(by=y_label, ascending=False)

                event_df.plot(kind='bar', x=x_label, y=y_label, ax=ax_chart, color=gc.get('BAR_CHARTS', 'BARS_COLOR'))
            except:
                print("No data in the", title, "chart")

    # Refresh the canvas to reflect the changes
    for ax in axes_list:
        ax.grid(axis='y', linestyle=gc.get('BAR_CHARTS', 'VERTICAL_LIGNES_STYLE'), 
                linewidth=gc.get('BAR_CHARTS', 'VERTICAL_LIGNES_WIDTH'), 
                color=gc.get('BAR_CHARTS', 'VERTICAL_LIGNES_COLOR'))

    bar_chart_canvas.draw()

def update_pie_chart(pie_chart, data : dict):
    # do not show the TOTAL_TIME to the pie chart 
    reference_amount = data.pop('TOTAL_TIME')

    try:
        ax = pie_chart.figure.axes[0]
        title = ax.get_title()
        ax.clear()
        ax.set_title(title)

        ax.pie(data.values(), labels=data.keys(), autopct='%1.1f%%')
    except:
        messagebox.showerror("Impossible to plot data", "There is no data to plot")
    finally:
        pie_chart.draw()

def on_configure(event, canvas):
    canvas.configure(scrollregion=canvas.bbox('all'))
#------------------------------------------------