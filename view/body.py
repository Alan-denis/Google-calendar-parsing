#------------------------------------------------
from tkinter import *
from tkinter import ttk, filedialog
#------------------------------------------------

#------------------------------------------------
from sources.handlers.event_handler import *
from sources.utils.config import *

from main import gui_conf as gc
from main import events_conf as ec
from main import conf_path
from main import config_obj
#------------------------------------------------

def only_show(root_frame : Tk, menu_frame : Frame, frame_to_show : Frame):

    for widget in root_frame.winfo_children():
        widget.grid_forget()

    menu_frame.grid(row=0, column=0, sticky="nsew", padx=(10, 0), pady=10)
    frame_to_show.grid(row=0, column=1, sticky="nsew", padx=(0, 10), pady=10)

# Function to populate the listbox with configurations
def populate_configurations_text(entry_box : Text, selected_conf : str):
    conf_file_path = os.path.join(conf_path, 'events' + '.ini')

    conf = ConfigParser()
    conf.read(conf_file_path)

    entry_box.delete(0.0, END)
    entry_box.insert(0.0, Config.from_ini_to_json(conf_file_path))

def select_csv_file(csv_entry : Entry):
    file_path = filedialog.askopenfilename(filetypes=[("ICS files", "*.ics")])

    if file_path != '':
        csv_entry.delete(0, END)
        config_obj.calendar_ics_file_path = file_path

        csv_entry.insert(END, config_obj.calendar_ics_file_path)

def save_configuration(conf_string):
    print(Config.from_json_to_ini(conf_string, "E:\OneDrive - Efrei\Grind\Projets\Google-calendar-parsing\\output.ini"))

def cancel_configuration():
    pass

def find_ini_files(directory):
    ini_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.ini'):
                ini_files.append(file[:-4])
    return ini_files

#------------------------------------------------
def start_gui():
    root = Tk()
    root.title(gc.get('APP', 'NAME'))
    root.minsize(gc.get('APP', 'MIN_HEIGHT'), gc.get('APP', 'MIN_WIDTH'))
    root.geometry(gc.get('APP', 'DIMENSIONS'))
    root.columnconfigure(1, weight=1)

    # Menu
    #-------------------------------------------------------------------------
    menu_frame = Frame(root, bg=gc.get('APP', 'BACKGROUND_LEFT_FRAME'), width=100)
    menu_frame.grid(row=0, column=0, sticky="nsew", padx=(10, 0), pady=10)

    # Buttons in Menu
    button = Button(menu_frame, text="Statistics", width=30,  command=lambda : only_show(root, menu_frame, right_frame))
    button.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

    button = Button(menu_frame, text="Configuration", width=30, command=lambda : only_show(root, menu_frame, conf_frame))
    button.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
    #-------------------------------------------------------------------------

    #Configuration
    #-------------------------------------------------------------------------
    # Button to populate the listbox with configurations
    conf_frame = Frame(root, bg=gc.get('APP', 'BACKGROUND_RIGHT_FRAME'))
    conf_frame.columnconfigure(0, weight=1)
    conf_frame.rowconfigure(1, weight=1)

    #-----------------------------------------
    csv_frame = Frame(conf_frame)
    csv_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=10)

    # Label and entry for CSV file path
    csv_label = Label(csv_frame, text="Input file:")
    csv_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

    csv_path_entry = Entry(csv_frame, width=100)
    csv_path_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
    csv_path_entry.insert(0, config_obj.calendar_ics_file_path)

    # Button to open file explorer and select CSV file
    select_csv_button = Button(csv_frame, text="...", width=3, command=lambda : select_csv_file(csv_path_entry))
    select_csv_button.grid(row=0, column=2, padx=(0, 10), pady=5, sticky="e")
    #-----------------------------------------
    
    #-----------------------------------------
    f = Frame(conf_frame)
    f.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

    populate_button = Button(f, text="See Configurations", width=30, command=lambda : populate_configurations_text(configurations_text, choice_filter.get()))
    populate_button.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

    ini_files = find_ini_files(conf_path)
    choice_filter = ttk.Combobox(f, width=15, values=ini_files)
    choice_filter.set(ini_files[0])
    choice_filter.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
    #-----------------------------------------

    # Listbox to display configurations
    configurations_text = Text(conf_frame, state=NORMAL)
    configurations_text.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
    
    #-----------------------------------------
    f = Frame(conf_frame)
    f.grid(row=3, column=0, padx=10, pady=10, sticky="nswe")

    # Button to add a configuration
    save_button = Button(f, text="Save configuration", width=30, bg='green', command=lambda : save_configuration(configurations_text.get(0.0, END)))
    save_button.grid(row=0, column=0, padx=10, pady=10, sticky="nswe")

    # Button to remove a configuration
    cancel_button = Button(f, text="Cancel modification", width=30, command=cancel_configuration, bg='red')
    cancel_button.grid(row=0, column=1, padx=10, pady=10, sticky="nswe")
    #-----------------------------------------
    #-------------------------------------------------------------------------

    # Right Frame
    #-------------------------------------------------------------------------
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
    
    # Checkbox for start date filter
    start_date_filter_var = BooleanVar()
    start_date_filter_checkbox = Checkbutton(filter_frame, text="Filter with start", variable=start_date_filter_var)
    start_date_filter_checkbox.grid(row=0, column=1, padx=10, pady=10)

    # Label for start date
    start_date_label = Label(filter_frame, text="Start Date:")
    start_date_label.grid(row=0, column=2, padx=10, pady=10)

    # Entry for start date
    start_date_entry = Entry(filter_frame, validate="key")
    start_date_entry.config(validatecommand=(root.register(lambda new_value: len(new_value) <= 10), "%P"))
    start_date_entry.grid(row=0, column=3, padx=10, pady=10)
    start_date_entry.insert(0, "DD-MM-YYY")
    start_date_entry.bind("<FocusOut>", lambda event: filter_date_on_leave(event, pie_chart, bar_chart_canvas, start_date_entry.get(), end_date_entry.get(), start_date_filter_var.get(), end_date_filter_var.get()))

    # Checkbox forstart date filter
    end_date_filter_var = BooleanVar()
    end_date_filter_checkbox = Checkbutton(filter_frame, text="Filter with end", variable=end_date_filter_var)
    end_date_filter_checkbox.grid(row=0, column=4, padx=10, pady=10)

    # Label for end date
    end_date_label = Label(filter_frame, text="End Date:")
    end_date_label.grid(row=0, column=5, padx=10, pady=10)

    # Entry for end date
    end_date_entry = Entry(filter_frame, validate="key")
    start_date_entry.config(validatecommand=(root.register(lambda new_value: len(new_value) <= 10), "%P"))
    end_date_entry.grid(row=0, column=6, padx=10, pady=10)
    end_date_entry.insert(0, "DD-MM-YYY")
    end_date_entry.bind("<FocusOut>", lambda event: filter_date_on_leave(event, pie_chart, bar_chart_canvas, start_date_entry.get(), end_date_entry.get(), start_date_filter_var.get(), end_date_filter_var.get())
    )

    # Canvas andscrollbar
    canvas = Canvas(right_frame)
    canvas.grid(row=1, column=0, columnspan=3, sticky="nsew")
    canvas.columnconfigure(0, weight=1)

    scrollbar = Scrollbar(right_frame, orient='vertical', command=canvas.yview, width=30)
    scrollbar.grid(row=0, column=1, rowspan=3, sticky='ns')
    canvas.configure(yscrollcommand=scrollbar.set)
    # canvas.bind('<Configure>', lambda event : on_configure(event, canvas))

    # Place pie chart
    pie_chart = GuiUtils.create_pie_chart(canvas, gc.get('PIE_CHART_BY_CATEGORY', 'NAME'), 0, 0)
    
    # Place bar charts
    bar_chart_canvas = GuiUtils.create_bar_charts(canvas, 1, 0, ec.sections())

    chart_data = pd.DataFrame({"x_label" : ['1'], "y_label": [72]})
    chart_data.plot(kind='bar', ax=bar_chart_canvas.figure.axes[0], color=gc.get('BAR_CHARTS', 'BARS_COLOR'))
    #-------------------------------------------------------------------------

    root.mainloop()
#------------------------------------------------