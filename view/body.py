#------------------------------------------------
from tkinter import *
from tkinter import ttk
#------------------------------------------------

#------------------------------------------------
from sources.handlers.event_handler import *
from sources.utils.config import *

from main import gui_conf as gc
from main import events_conf as ec
#------------------------------------------------

def only_show(Frame):
    Frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=10)
    right_frame.grid_forget()

#------------------------------------------------
def start_gui():
    root = Tk()
    root.title(gc.get('APP', 'NAME'))
    root.minsize(gc.get('APP', 'MIN_HEIGHT'), gc.get('APP', 'MIN_WIDTH'))
    root.geometry(gc.get('APP', 'DIMENSIONS'))
    root.columnconfigure(1, weight=1)

    # Left Frame
    left_frame = Frame(root, bg=gc.get('APP', 'BACKGROUND_LEFT_FRAME'), width=100)
    left_frame.grid(row=0, column=0, sticky="nsew", padx=(10, 0), pady=10)

    # Buttons in left frame
    button = Button(left_frame, text="Statistics", command=None, width=30)
    button.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

    button = Button(left_frame, text="View 2", width=30, command=lambda : hide_statistics)
    button.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

    # Right Frame
    right_frame = Frame(root, bg=gc.get('APP', 'BACKGROUND_RIGHT_FRAME'))
    right_frame.grid(row=0, column=1, sticky="nsew", padx=(0, 10), pady=10)
    right_frame.columnconfigure(0, weight=1)
    right_frame.rowconfigure(1, weight=1)

    # Filter Frame
    filter_frame = Frame(right_frame)  # Set background color for visibility
    filter_frame.grid(row=0, column=0, sticky="nsew")

    # Combobox for filter
    activities = gc.get('FILTER_BAR', 'FILTER_CHOICES').split(', ')
    choice_filter = ttk.Combobox(filter_frame, width=15, values=activities)
    choice_filter.grid(row=0, column=0, padx=10, pady=10)
    choice_filter.bind('<<ComboboxSelected>>', lambda event: activity_filter(event, choice_filter.get()))

    # Label for start date
    start_date_label = Label(filter_frame, text="Start Date:")
    start_date_label.grid(row=0, column=1, padx=10, pady=10)

    # Entry for start date
    start_date_entry = Entry(filter_frame)
    start_date_entry.grid(row=0, column=2, padx=10, pady=10)
    start_date_entry.insert(0, "YYYY-MM-DD")
    start_date_entry.bind("<FocusOut>", lambda event: filter_date_on_leave(event, start_date_entry.get(), end_date_entry.get(), pie_chart, bar_chart_ax_list))

    # Label for end date
    end_date_label = Label(filter_frame, text="End Date:")
    end_date_label.grid(row=0, column=3, padx=10, pady=10)

    # Entry for end date
    end_date_entry = Entry(filter_frame)
    end_date_entry.grid(row=0, column=4, padx=10, pady=10)
    end_date_entry.insert(0, "YYYY-MM-DD")
    end_date_entry.bind("<FocusOut>", lambda event: filter_date_on_leave(event, start_date_entry.get(), end_date_entry.get(), pie_chart, bar_chart_ax_list))

    # Canvas and scrollbar
    canvas = Canvas(right_frame, bg='pink', height=1000)
    canvas.grid(row=1, column=0, columnspan=3, sticky="nsew")
    canvas.columnconfigure(0, weight=1)
    canvas.rowconfigure(1, weight=1)

    scrollbar = Scrollbar(right_frame, orient='vertical', command=canvas.yview, width=30)
    scrollbar.grid(row=0, column=1, rowspan=3, sticky='ns')
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind('<Configure>', lambda event : on_configure(event, canvas))

    inner_frame = Frame(canvas, bg='green')
    inner_frame.update_idletasks()
    canvas.create_window((0, 0), window=inner_frame, anchor="center")

    # Place pie chart
    pie_chart = create_pie_chart(inner_frame, gc.get('PIE_CHART_BY_CATEGORY', 'NAME'), 0, 0)
    
    # Place bar charts
    bar_chart_ax_list = create_bar_charts(inner_frame, 1, 0, ec.sections())

    root.mainloop()
#------------------------------------------------