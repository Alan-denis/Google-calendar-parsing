#------------------------------------------------
import matplotlib.pyplot as plt
from tkinter import *
#------------------------------------------------

#------------------------------------------------
#------------------------------------------------

#------------------------------------------------
def update_pie_chart(canvas, data : dict):
    data.pop('TOTAL_TIME')

    # Plot the new data
    fig, ax = plt.subplots()
    ax.pie(data.values(), labels=data.keys(), autopct='%1.1f%%')
    ax.set_title('Time Distribution')

    # Redraw the canvas with the updated plot
    canvas.figure = fig
    canvas.draw()
#------------------------------------------------