# --- UNDER CONSTRUCTION --- #
"""File contains methods to update & save metadata

Class: MetadataInterface"""

import json
import tkinter as tk


BUTTON_FONT = ('Arial',12,'bold')
LABEL_FONT = ('Arial',14,'normal')
ENTRY_FONT = ('Arial',12,'normal')


class MetadataInterface:
    """Contains methods to display (using graphical interface via tkinter)
    searched metadata using experiment ID. methods to update & save metadata.
    
    Methods: update_metadata, save_metadata, GUI, search_experiment,
    display_experiment"""

    def update_metadata(self):
        """Updates the metadata with the new values added to the entry boxes in the GUI."""
        self.template = {}
        for key, entry in self.metadata.items():
            new_value = entry.get()
            if key == "Duration":
                new_value = int(new_value)
            self.template[key] = new_value

        self.new_metadata = {self.exp_ID: self.template}
        self.save_metadata()
    
    def save_metadata(self, metadata=""):
        """Saves metadata of experiment in metadata.json file.

        If accessing method outside of GUI:
        Parameter: metadata (nested dictionary)
        """
        if metadata != "":
            self.new_metadata = metadata
        
        try:
            with open("metadata.json", 'r') as json_file:
                data = json.load(json_file)
        except FileNotFoundError:
            with open("metadata.json", 'w') as json_file:
                json.dump(self.new_metadata, json_file, indent=4)
        else:
            data.update(self.new_metadata)
            with open("metadata.json", "w") as json_file:
                json.dump(data, json_file, indent=4)

        print("metadata has been saved successfully.")

    def GUI(self):
        """Displays a graphical user interface for the user to search and edit
        existing metadata.
        """
        window = tk.Tk()
        window.title("Search Metadata")
        window.geometry("500x300")

        exp_label = tk.Label(text="Metadata for experiment: ", font=LABEL_FONT)
        exp_label.grid(column=0, row=0)

        self.exp_input = tk.Entry(font=ENTRY_FONT)
        self.exp_input.insert(0, "type experiment ID")
        self.exp_input.grid(column=1, row=0)
        

        exp_button = tk.Button(text="Search", font=BUTTON_FONT, command=self.search_experiment)
        exp_button.grid(column=2, row=0)

        window.mainloop()
    
    def search_experiment(self):
        """Searches for experiment with the experiment ID entry,
        & checks if the experiment ID exists.
        """
        try:
            with open(file="metadata.json", mode="r") as json_file:
                content = json.load(json_file)
        except FileNotFoundError as e:
            print("There is no metadata yet.")
            return None
        
        try:
            self.exp_ID = self.exp_input.get().strip()
            self.exp_data = content[self.exp_ID]
        except KeyError:
            print("Invalid Experiment ID.")
        else:
            self.display_experiment()    

    def display_experiment(self):
        """Displays current metadata, values are displayed in editable entry boxes.

        All edits will be saved when clicking the 'Submit' button.
        """
        row_c = 1
        self.metadata = {}
        for key, value in self.exp_data.items():
            key_str = str(key).replace("_", " ")
            label_text = f"{key_str}: "
            label = tk.Label(text=label_text, font=LABEL_FONT)
            label.grid(column=0, row=row_c)
            entry = tk.Entry(font=ENTRY_FONT)
            entry.grid(column=1, row=row_c)
            entry.insert(0, value)

            if key == "Duration":
                hour_label = tk.Label(text="hour(s)", font=LABEL_FONT)
                hour_label.grid(column=2, row=row_c)
            
            self.metadata[key] = entry
            row_c += 1
        sumbit_button = tk.Button(text="Submit & Save", font=BUTTON_FONT, command=self.update_metadata)
        sumbit_button.grid(column=1, row=row_c)

# MetadataInterface().GUI()
