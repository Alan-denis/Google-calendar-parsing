#------------------------------------------------
import matplotlib.pyplot as plt
from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
#------------------------------------------------

#------------------------------------------------
from main import gui_conf
from main import events_conf
#------------------------------------------------

#------------------------------------------------
def create_bar_chart(master, chart_name, start_row, index):

    chart_data = pd.DataFrame({'Label': ['0'], 'Value': [0]})
    
    fig, ax = plt.subplots()
    chart_data.plot(kind='bar', ax=ax)
    ax.set_title(chart_name)
    ax.set_xlabel('Labels')
    ax.set_ylabel('Values')

    bar_chart = FigureCanvasTkAgg(fig, master=master)
    bar_chart.draw()
    bar_chart.get_tk_widget().grid(row=index+start_row, column=0, padx=10, pady=10, sticky="nsew")
    
    return ax
#------------------------------------------------