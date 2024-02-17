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
#------------------------------------------------



#------------------------------------------------
def start_gui():
    root = Tk()
    root.title("Calendar analitics")
    root.minsize(700, 300)
    root.geometry("1000x600")

    #------------------------------------------------
    left_frame = Frame(root, bg="lightgray", width=100)
    left_frame.pack(side=LEFT, fill=Y)

    #------------------
    button = Button(left_frame, text="View 1", command=None, width=30)
    button.pack(padx=10, pady=10)

    button = Button(left_frame, text="View 2", command=None, width=30)
    button.pack(padx=10, pady=10)
    #------------------
    #------------------------------------------------

    #------------------------------------------------
    right_frame = Frame(root)
    right_frame.pack()

    #------------------

    # Create filter bar
    filter_frame = Frame(right_frame, height=70)
    filter_frame.pack(fill=X)

    activities = gui_conf.get('FILTER_BAR', 'FILTER_CHOICES').split(', ')
    choice_filter = ttk.Combobox(filter_frame, width = 15, values=activities) 
    choice_filter.pack(side=LEFT,padx=5, pady=5)
    choice_filter.bind('<<ComboboxSelected>>', lambda event: activity_filter(event, choice_filter.get()))
    
    # Entry widget for filtering by task/event
    start_date_entry = Entry(filter_frame)
    start_date_entry.pack(side=LEFT,padx=5, pady=5, fill=X, expand=True)
    start_date_entry.insert(0, "start-date [YYYY-MM-DD HH:MM]")
    start_date_entry.bind("<FocusOut>", lambda event: start_date_on_leave(event, start_date_entry.get(), canvas))

    # Entry widget for filtering by task/event
    end_date_entry = Entry(filter_frame)
    end_date_entry.pack(side=LEFT, padx=5, pady=5, fill=X, expand=True)
    end_date_entry.insert(0, "end-date [YYYY-MM-DD HH:MM]")
    end_date_entry.bind("<FocusOut>", lambda event : end_date_on_leave(event, end_date_entry.get(), canvas))
    #------------------

    #------------------
    fig, ax = plt.subplots()
    ax.pie(["1.0"], labels=["Empty"], autopct='%1.1f%%')
    ax.set_title('Time Distribution')

    canvas = FigureCanvasTkAgg(fig, master=right_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=BOTH, expand=True)
    #------------------
    #------------------------------------------------

    root.mainloop()
#------------------------------------------------



#------------------------------------------------
#------------------------------------------------