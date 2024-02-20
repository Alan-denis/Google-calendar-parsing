#------------------------------------------------
from tkinter import *
from tkinter import ttk
import sys
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
#------------------------------------------------

#------------------------------------------------
from sources.handlers.event_handler import *
from sources.utils.config import *

from main import gui_conf
from main import events_conf
#------------------------------------------------

#------------------------------------------------
def start_gui():
    root = Tk()
    root.title(gui_conf.get('APP', 'NAME'))
    root.minsize(gui_conf.get('APP', 'MIN_HEIGHT'), gui_conf.get('APP', 'MIN_WIDTH'))
    root.geometry(gui_conf.get('APP', 'DIMENSIONS'))
    root.columnconfigure(1, weight=1)

    # Left Frame
    left_frame = Frame(root, bg=gui_conf.get('APP', 'BACKGROUND_LEFT_FRAME'), width=100)
    left_frame.grid(row=0, column=0, sticky="nsew", padx=(10, 0), pady=10)

    # Buttons in left frame
    button = Button(left_frame, text="Statistics", command=None, width=30)
    button.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

    button = Button(left_frame, text="View 2", command=None, width=30)
    button.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

    # Right Frame
    right_frame = Frame(root, bg=gui_conf.get('APP', 'BACKGROUND_RIGHT_FRAME'))
    right_frame.grid(row=0, column=1, sticky="nsew", padx=(0, 10), pady=10)
    right_frame.columnconfigure(0, weight=1)
    right_frame.rowconfigure(0, weight=0)  # Adjusted weight to 0 to prevent the filter_frame from expanding vertically
    right_frame.rowconfigure(1, weight=1)

    # Filter Frame
    filter_frame = Frame(right_frame, bg='blue')  # Set background color for visibility
    filter_frame.grid(row=0, column=0, sticky="ew")

    # Combobox for filter
    activities = gui_conf.get('FILTER_BAR', 'FILTER_CHOICES').split(', ')
    choice_filter = ttk.Combobox(filter_frame, width=15, values=activities)
    choice_filter.grid(row=0, column=0, padx=10, pady=10)

    # Entry for start date
    start_date_entry = Entry(filter_frame)
    start_date_entry.grid(row=0, column=1, padx=10, pady=10)
    start_date_entry.insert(0, "start-date [YYYY-MM-DD HH:MM]")

    # Entry for end date
    end_date_entry = Entry(filter_frame)
    end_date_entry.grid(row=0, column=2, padx=10, pady=10)
    end_date_entry.insert(0, "end-date [YYYY-MM-DD HH:MM]")

    # Canvas and scrollbar
    canvas = Canvas(right_frame)
    canvas.grid(row=1, column=0, sticky="nsew", padx=(0, 20), pady=(0, 20))  # Adjusted padx and pady
    right_frame.grid_rowconfigure(1, weight=1)  # Make canvas expand vertically
    right_frame.grid_columnconfigure(0, weight=1)  # Make canvas expand horizontally

    scrollbar = Scrollbar(right_frame, orient='vertical', command=canvas.yview)
    scrollbar.grid(row=1, column=1, sticky='ns')
    canvas.configure(yscrollcommand=scrollbar.set)

    inner_frame = Frame(canvas)
    canvas.create_window((0, 0), window=inner_frame, anchor='nw')

    # Update inner frame size
    inner_frame.update_idletasks()

    # Function to adjust scroll region
    def on_configure(event):
        canvas.configure(scrollregion=canvas.bbox('all'))

    canvas.bind('<Configure>', on_configure)

    # Place pie chart
    pie_chart_ax = create_pie_chart(inner_frame, gui_conf.get('PIE_CHART_BY_CATEGORY', 'NAME'), 0, 0)

    # Place bar charts
    bar_chart_ax_list = create_bar_charts(inner_frame, 1, 0, events_conf.sections())

    root.mainloop()




