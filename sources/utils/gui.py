#------------------------------------------------
import matplotlib.pyplot as plt
from tkinter import *
#------------------------------------------------

#------------------------------------------------
#------------------------------------------------

#------------------------------------------------
def update_pie_chart(canvas, data : dict):
    reference_amount = data['TOTAL_TIME']
    # do not show the TOTAL_TIME to the pie chart 
    data.pop('TOTAL_TIME')

    # Plot the new data
    fig, ax = plt.subplots()
    ax.pie(data.values(), labels=data.keys(), autopct='%1.1f%%')
    ax.set_title('Time Distribution')

    # Redraw the canvas with the updated plot
    canvas.figure = fig
    canvas.draw()
#------------------------------------------------