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

    #------------------------------------------------
    left_frame = Frame(root, bg=gui_conf.get('APP', 'BACKGROUND_LEFT_FRAME'), width=100)
    left_frame.grid(row=0, column=0, sticky="nsew", columnspan=1)

    #------------------
    button = Button(left_frame, text="Statistics", command=None, width=30)
    button.grid(row=0, column=0, padx=10, pady=10)

    button = Button(left_frame, text="View 2", command=None, width=30)
    button.grid(row=1, column=0, padx=10, pady=10)
    #------------------
    #------------------------------------------------

    #------------------------------------------------
    right_frame = Frame(root, bg=gui_conf.get('APP', 'BACKGROUND_RIGHT_FRAME'))
    right_frame.grid(row=0, column=1, columnspan=1)
    right_frame.rowconfigure(0, weight=1)
    right_frame.columnconfigure(0, weight=1)

    #------------------
    # Create filter bar
    filter_frame = Frame(right_frame, height=70)
    filter_frame.grid(row=0, column=0, sticky="nsew")

    activities = gui_conf.get('FILTER_BAR', 'FILTER_CHOICES').split(', ')
    choice_filter = ttk.Combobox(filter_frame, width = 15, values=activities) 
    choice_filter.grid(row=0, column=1)
    choice_filter.bind('<<ComboboxSelected>>', lambda event: activity_filter(event, choice_filter.get()))
    
    # Entry widget for filtering by task/event
    start_date_entry = Entry(filter_frame)
    start_date_entry.grid(row=0, column=2)
    start_date_entry.insert(0, "start-date [YYYY-MM-DD HH:MM]")
    start_date_entry.bind("<FocusOut>", lambda event: filter_date_on_leave(event, start_date_entry.get(), end_date_entry.get(), pie_chart, bar_chart_ax_list))

    # Entry widget for filtering by task/event
    end_date_entry = Entry(filter_frame)
    end_date_entry.grid(row=0, column=3)
    end_date_entry.insert(0, "end-date [YYYY-MM-DD HH:MM]")
    end_date_entry.bind("<FocusOut>", lambda event : filter_date_on_leave(event, start_date_entry.get(), end_date_entry.get(), pie_chart, bar_chart_ax_list))
    #------------------

    #------------------
    canvas = Canvas(right_frame, width=1000, height=1000)
    canvas.grid(row=1, column=0, rowspan=2, sticky="nsew")

    # Create a scrollbar and associate it with the canvas
    scrollbar = Scrollbar(right_frame, orient='vertical', command=canvas.yview)
    scrollbar.grid(row=0, column=1, sticky='ns', rowspan=2)
    canvas.configure(yscrollcommand=scrollbar.set)

    # Bind the event handler to configure the scrollregion
    canvas.bind('<Configure>', lambda event : on_configure(event, canvas))

    # Create a frame to contain the widgets
    inner_frame = Frame(canvas, bg='green')

    # Set the size of the inner frame to match its contents
    inner_frame.update_idletasks()  # Ensure all widgets are properly placed
    canvas.create_window((0, 0), window=inner_frame, anchor='nw')
    #------------------

    #------------------
    fig, ax = plt.subplots()
    ax.pie(["1.0"], labels=["Empty"], autopct='%1.1f%%')
    ax.set_title('Time Distribution')

    pie_chart = FigureCanvasTkAgg(fig, master=inner_frame)
    pie_chart.draw()
    pie_chart.get_tk_widget().grid(row=1, column=0, sticky="nsew")
    #------------------

    #------------------
    bar_chart_ax_list = []

    for index, section in enumerate(events_conf.sections()):
        bar_chart_ax_list.append(create_bar_chart(inner_frame, section, 2, index))
    #------------------
    #------------------------------------------------

    root.mainloop()
#------------------------------------------------



#------------------------------------------------
#------------------------------------------------