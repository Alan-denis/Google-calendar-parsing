#------------------------------------------------
import matplotlib.pyplot as plt
from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import math
#------------------------------------------------

#------------------------------------------------
from main import gui_conf as gf
#------------------------------------------------

#------------------------------------------------
class GuiUtils:

    def create_pie_chart(master, chart_name, row, column):

        fig, ax = plt.subplots()
        ax.set_title(chart_name)

        pie_chart = FigureCanvasTkAgg(fig, master=master)
        pie_chart.draw()
        pie_chart.get_tk_widget().grid(row=row, column=column, sticky="nsew")
        return pie_chart

    def create_bar_charts(master, row: int, column: int, chart_names: list, figsize=(10, 8)) -> list:
        num_charts = len(chart_names)
        num_cols = 2  # Fixed number of columns for the subplot grid
        num_rows = math.ceil(num_charts / num_cols)  # Calculate the number of rows needed for the subplot grid

        x_label = "Activities"
        y_label = "Hours"

        fig, axs = plt.subplots(nrows=num_rows, ncols=num_cols, figsize=figsize)
        fig.tight_layout(pad=6)

        for ax, name in zip(axs.flat, chart_names):
            if name:
                ax.set_title(name)
                ax.set_xlabel(x_label)
                ax.set_ylabel(y_label)

        canvas = FigureCanvasTkAgg(fig, master=master)
        canvas.draw()
        canvas.get_tk_widget().grid(row=row, column=column, sticky="nsew")

        return canvas
    
    