import pandas as pd
from tkinter import *
from tkinter import ttk
import tkinter.filedialog as fd
from tkinter import messagebox
from itertools import product
from itertools import chain
import numpy as np
import sqlite3
import os
import math
from pda_to_vtk import *




# Create an instance of tkinter frame or window
win = Tk()

# Set the geometry of tkinter frame
win.geometry("900x1000")

# store user input
year = StringVar()
mode = StringVar()
emission = StringVar()
# Enter frame
enter = ttk.Frame(win)
enter.pack(padx=40, pady=40, fill='x', expand=False)

# register year entry constrains
reg = win.register(year_limit)  # Register Entry validation function.

# year entry
year_label = ttk.Label(enter, text="Run Year:")
year_label.pack(fill=None, expand=False)

year_entry = ttk.Entry(enter, textvariable=year, validate='key', validatecommand=(reg, '%P'))  # text variable is stored in variable 'year', with constraints to ensure 4 digit number is entered
year_entry.pack(fill=None, expand=False)
year_entry.focus()
# mode entry
mode_label = ttk.Label(enter, text="Run Mode (lowest/average):")
mode_label.pack(fill=None, expand=False)
# mode_entry = ttk.Entry(enter, textvariable=mode, validate='key')  # text variable is stored in variable 'mode', no constraint
# mode_entry.pack(fill=None, expand=False)
# mode_entry.focus()

mode = StringVar(enter)
mode.set("lowest") # default value
mode_drop = OptionMenu(enter, mode,"lowest", "average")
mode_drop.pack()


emission_label = ttk.Label(enter, text="Emission Mode (running/starting):")
emission_label.pack(fill=None, expand=False)
# emission_entry = ttk.Entry(enter, textvariable=emission, validate='key')  # text variable is stored in variable 'mode', no constraint
# emission_entry.pack(fill=None, expand=False)
# emission_entry.focus()
emission = StringVar(enter)
emission.set("running") # default value
emission_drop = OptionMenu(enter, emission, "running", "starting")
emission_drop.pack()


# Destroy window when click cross
win.protocol("WM_DELETE_WINDOW", Close)

# Add a Label widget
label = Label(win, text="Enter the Year of Study, Run Mode, Emission Mode and proceed step-by-step below", font='Aerial 11')
label.pack(pady=5)


# Add a Button Widget
ttk.Button(win, text="Convert pda to vtk", command=step1_getmetdata).pack(side= TOP, pady=10, ipady=20)

ttk.Button(win, text="RUN STEP2: Select the Speed file (Enter correct Year in user input)", command=step2_addspeed).pack(side= TOP, pady=20)

ttk.Button(win, text="RUN STEP3: Query data from database", command=step3_lookupdatabase).pack(side= TOP, pady=10, ipady=20)

ttk.Button(win, text="RUN STEP4: Lookup and Export Result as Excel", command=step4_joindata).pack(side= TOP, pady=10, ipady=20)

win.mainloop()
