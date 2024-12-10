"""File contains GUI for main GUI of program, has methods to start new experiment.

Class: MeasuremntInterface"""

import tkinter as tk
from tkinter import messagebox as tk_messagebox

from edit_metadata import MetadataInterface


BUTTON_FONT = ('Arial',12,'bold')
LABEL_FONT = ('Arial',14,'normal')
ENTRY_FONT = ('Arial',12,'normal')


class MeasurementInterface:
    """Contains methods to display (using graphical interface via tkinter)
    Main GUI, start a new experiment, & navigate to Metadata GUI
    (via MetadataInterface class).
    
    Methods: __init__, new_GUI, start_experiment, save_popup, open_MD_Interface.
    """
    def __init__(self):
        """GUI of measurement program. Buttons to start a new experiment
        or search existing metadata.
        """
        self.window = tk.Tk()
        self.window.title("Measurements")
        self.window.geometry("400x200")

        self.title = tk.Label(text="Measure Air Quality", font=('Arial',16,'bold'))
        self.title.grid(column=0, row=0, columnspan=3)

        self.label = tk.Label(text="What would you like to do?", font=ENTRY_FONT)
        self.label.grid(column=0, row=1, columnspan=3, pady=10)

        self.new_button = tk.Button(text="New Experiment", font=BUTTON_FONT, command=self.new_GUI)
        self.new_button.grid(column=1, row=2, padx=5)

        self.search_button = tk.Button(text="Search Metadata", font=BUTTON_FONT, command=self.open_MD_interface)
        self.search_button.grid(column=2, row=2)
        self.window.mainloop()
    
    def new_GUI(self):
        """GUI of new experiment to collect the specs of experiment
        Requires to input of location of sensor & duration of experiment (hrs).
        """
        self.search_button.destroy()
        self.new_button.destroy()
        self.title.destroy()
        
        self.window.geometry("400x200")

        title_label = tk.Label(text="New Experiment", font=('Arial',16,'bold'))
        title_label.grid(column=0, row=0, columnspan=3)
        info_label = tk.Label(text="Please provide the following information:",
                              font=('Arial',12,'normal'))
        info_label.grid(column=0, row=1, columnspan=3)

        location_label = tk.Label(text="Location of sensor: ", font=LABEL_FONT)
        location_label.grid(column=0, row=3)
        self.location_entry = tk.Entry(font=ENTRY_FONT)
        self.location_entry.grid(column=2, row=3)

        duration_label = tk.Label(text="Duration (hr): ", font=LABEL_FONT)
        duration_label.grid(column=0, row=4)
        self.duration_entry = tk.Entry(font=ENTRY_FONT)
        self.duration_entry.grid(column=2, row=4)

        self.start_button = tk.Button(text="Start", command=self.start_experiment, font=BUTTON_FONT)
        self.start_button.grid(column=2, row=5)

    def start_experiment(self):
        """Gets and saves location and duration entries from Tk entry boxs
        into the MeasurementInterface class.
        Destroys tkinter window (breaks mainloop) to allow readings to be collected.
        """
        MeasurementInterface.location = self.location_entry.get()
        MeasurementInterface.duration = self.duration_entry.get()

        self.window.destroy()
    
    def save_popup(self, ID):
        """Tkinter messagebox is displayed on screen to tell user
        that the measured data has been saved as a CSV file
        
        Parameters: ID (str) (of experiment)
        """
        saved_message = f"CSV file has been saved successfully.\nExperiment ID: {ID}"
        tk_messagebox.showinfo(message=saved_message)

    def open_MD_interface(self):
        """Destroys Measurment GUI window to open MetadataInterface GUI."""
        self.window.destroy()

        MetadataInterface().GUI()
