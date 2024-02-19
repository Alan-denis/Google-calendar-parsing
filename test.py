import tkinter as tk

root = tk.Tk()

# Create a canvas
canvas = tk.Canvas(root, bg='blue', width=400, height=300)
canvas.grid(row=0, column=0, sticky='nsew')  # Expand to fill entire space

# Create a frame inside the canvas
inner_frame = tk.Frame(canvas, bg='green')
inner_frame.grid(row=0, column=0, sticky='nsew')  # Expand to fill entire space

# Add some widgets to the inner frame
label = tk.Label(inner_frame, text="Hello, World!", bg='green')
label.pack(padx=10, pady=10)

root.mainloop()
